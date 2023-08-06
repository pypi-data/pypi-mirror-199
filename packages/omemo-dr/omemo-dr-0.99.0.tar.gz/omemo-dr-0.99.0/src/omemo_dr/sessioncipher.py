from __future__ import annotations

from typing import Union

import logging

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import modes

from .ecc.curve import Curve
from .ecc.djbec import CurvePublicKey
from .exceptions import DuplicateMessageException
from .exceptions import InvalidMessageException
from .exceptions import NoSessionException
from .kdf.messagekeys import MessageKeys
from .protocol.prekeywhispermessage import PreKeyWhisperMessage
from .protocol.whispermessage import WhisperMessage
from .ratchet.chainkey import ChainKey
from .sessionbuilder import SessionBuilder
from .state.identitykeystore import IdentityKeyStore
from .state.prekeystore import PreKeyStore
from .state.sessionrecord import SessionRecord
from .state.sessionstate import SessionState
from .state.sessionstore import SessionStore
from .state.signedprekeystore import SignedPreKeyStore

logger = logging.getLogger(__name__)


class SessionCipher:
    def __init__(
        self,
        sessionStore: SessionStore,
        preKeyStore: PreKeyStore,
        signedPreKeyStore: SignedPreKeyStore,
        identityKeyStore: IdentityKeyStore,
        recipientId: str,
        deviceId: int,
    ) -> None:
        self.sessionStore = sessionStore
        self.preKeyStore = preKeyStore
        self.recipientId = recipientId
        self.deviceId = deviceId
        self.sessionBuilder = SessionBuilder(
            sessionStore,
            preKeyStore,
            signedPreKeyStore,
            identityKeyStore,
            recipientId,
            deviceId,
        )

    def encrypt(
        self, paddedMessage: Union[bytes, str]
    ) -> Union[WhisperMessage, PreKeyWhisperMessage]:
        if isinstance(paddedMessage, str):
            paddedMessage = paddedMessage.encode()

        paddedMessage = bytearray(paddedMessage)

        sessionRecord = self.sessionStore.loadSession(self.recipientId, self.deviceId)
        sessionState = sessionRecord.getSessionState()
        chainKey = sessionState.getSenderChainKey()
        messageKeys = chainKey.getMessageKeys()
        senderEphemeral = sessionState.getSenderRatchetKey()
        previousCounter = sessionState.getPreviousCounter()
        sessionVersion = sessionState.getSessionVersion()

        ciphertextBody = self.getCiphertext(sessionVersion, messageKeys, paddedMessage)

        ciphertextMessage = WhisperMessage.new(
            sessionVersion,
            messageKeys.getMacKey(),
            senderEphemeral,
            chainKey.getIndex(),
            previousCounter,
            ciphertextBody,
            sessionState.getLocalIdentityKey(),
            sessionState.getRemoteIdentityKey(),
        )

        if sessionState.hasUnacknowledgedPreKeyMessage():
            items = sessionState.getUnacknowledgedPreKeyMessageItems()
            localRegistrationid = sessionState.getLocalRegistrationId()

            ciphertextMessage = PreKeyWhisperMessage.new(
                sessionVersion,
                localRegistrationid,
                items.getPreKeyId(),
                items.getSignedPreKeyId(),
                items.getBaseKey(),
                sessionState.getLocalIdentityKey(),
                ciphertextMessage,
            )

        sessionState.setSenderChainKey(chainKey.getNextChainKey())
        self.sessionStore.storeSession(self.recipientId, self.deviceId, sessionRecord)

        return ciphertextMessage

    def decryptMsg(self, ciphertext: WhisperMessage) -> bytes:
        if not self.sessionStore.containsSession(self.recipientId, self.deviceId):
            raise NoSessionException(
                "No session for: %s, %s" % (self.recipientId, self.deviceId)
            )

        sessionRecord = self.sessionStore.loadSession(self.recipientId, self.deviceId)
        plaintext = self.decryptWithSessionRecord(sessionRecord, ciphertext)

        self.sessionStore.storeSession(self.recipientId, self.deviceId, sessionRecord)

        return plaintext

    def decryptPkmsg(self, ciphertext: PreKeyWhisperMessage) -> bytes:
        sessionRecord = self.sessionStore.loadSession(self.recipientId, self.deviceId)
        unsignedPreKeyId = self.sessionBuilder.process(sessionRecord, ciphertext)
        plaintext = self.decryptWithSessionRecord(
            sessionRecord, ciphertext.getWhisperMessage()
        )

        self.sessionStore.storeSession(self.recipientId, self.deviceId, sessionRecord)

        if unsignedPreKeyId is not None:
            self.preKeyStore.removePreKey(unsignedPreKeyId)

        return plaintext

    def decryptWithSessionRecord(
        self, sessionRecord: SessionRecord, cipherText: WhisperMessage
    ) -> bytes:
        previousStates = sessionRecord.getPreviousSessionStates()
        exceptions: list[Exception] = []
        try:
            sessionState = SessionState(sessionRecord.getSessionState())
            plaintext = self.decryptWithSessionState(sessionState, cipherText)
            sessionRecord.setState(sessionState)
            return plaintext
        except InvalidMessageException as e:
            exceptions.append(e)

        for i in range(0, len(previousStates)):
            previousState = previousStates[i]
            try:
                promotedState = SessionState(previousState)
                plaintext = self.decryptWithSessionState(promotedState, cipherText)
                previousStates.pop(i)
                sessionRecord.promoteState(promotedState)
                return plaintext
            except InvalidMessageException as e:
                exceptions.append(e)

        raise InvalidMessageException("No valid sessions", exceptions)

    def decryptWithSessionState(
        self, sessionState: SessionState, ciphertextMessage: WhisperMessage
    ) -> bytes:
        if not sessionState.hasSenderChain():
            raise InvalidMessageException("Uninitialized session!")

        messageVersion = ciphertextMessage.getMessageVersion()
        if messageVersion != sessionState.getSessionVersion():
            raise InvalidMessageException(
                "Message version %s, but session version %s"
                % (
                    ciphertextMessage.getMessageVersion,
                    sessionState.getSessionVersion(),
                )
            )

        theirEphemeral = ciphertextMessage.getSenderRatchetKey()
        counter = ciphertextMessage.getCounter()
        chainKey = self.getOrCreateChainKey(sessionState, theirEphemeral)
        messageKeys = self.getOrCreateMessageKeys(
            sessionState, theirEphemeral, chainKey, counter
        )

        ciphertextMessage.verifyMac(
            sessionState.getRemoteIdentityKey(),
            sessionState.getLocalIdentityKey(),
            messageKeys.getMacKey(),
        )

        plaintext = self.getPlaintext(
            messageVersion, messageKeys, ciphertextMessage.getBody()
        )
        sessionState.clearUnacknowledgedPreKeyMessage()

        return plaintext

    def getOrCreateChainKey(
        self, sessionState: SessionState, ECPublickKey_theirEphemeral: CurvePublicKey
    ) -> ChainKey:
        theirEphemeral = ECPublickKey_theirEphemeral
        if sessionState.hasReceiverChain(theirEphemeral):
            return sessionState.getReceiverChainKey(theirEphemeral)
        else:
            rootKey = sessionState.getRootKey()
            ourEphemeral = sessionState.getSenderRatchetKeyPair()
            receiverChain = rootKey.createChain(theirEphemeral, ourEphemeral)
            ourNewEphemeral = Curve.generateKeyPair()
            senderChain = receiverChain[0].createChain(theirEphemeral, ourNewEphemeral)

            sessionState.setRootKey(senderChain[0])
            sessionState.addReceiverChain(theirEphemeral, receiverChain[1])
            sessionState.setPreviousCounter(
                max(sessionState.getSenderChainKey().getIndex() - 1, 0)
            )
            sessionState.setSenderChain(ourNewEphemeral, senderChain[1])
            return receiverChain[1]

    def getOrCreateMessageKeys(
        self,
        sessionState: SessionState,
        ECPublicKey_theirEphemeral: CurvePublicKey,
        chainKey: ChainKey,
        counter: int,
    ) -> MessageKeys:
        theirEphemeral = ECPublicKey_theirEphemeral
        if chainKey.getIndex() > counter:
            if sessionState.hasMessageKeys(theirEphemeral, counter):
                return sessionState.removeMessageKeys(theirEphemeral, counter)
            else:
                raise DuplicateMessageException(
                    "Received message with old counter: %s, %s"
                    % (chainKey.getIndex(), counter)
                )

        if counter - chainKey.getIndex() > 2000:
            raise InvalidMessageException("Over 2000 messages into the future!")

        while chainKey.getIndex() < counter:
            messageKeys = chainKey.getMessageKeys()
            sessionState.setMessageKeys(theirEphemeral, messageKeys)
            chainKey = chainKey.getNextChainKey()

        sessionState.setReceiverChainKey(theirEphemeral, chainKey.getNextChainKey())
        return chainKey.getMessageKeys()

    def getCiphertext(
        self, version: int, messageKeys: MessageKeys, plainText: bytearray
    ) -> bytes:
        cipher = AESCipher(messageKeys.getCipherKey(), messageKeys.getIv())
        return cipher.encrypt(bytes(plainText))

    def getPlaintext(
        self, version: int, messageKeys: MessageKeys, cipherText: bytes
    ) -> bytes:
        cipher = AESCipher(messageKeys.getCipherKey(), messageKeys.getIv())
        return cipher.decrypt(cipherText)


class AESCipher:
    def __init__(self, key: bytes, iv: bytes) -> None:
        self.key = key
        self.iv = iv
        self.cipher = Cipher(
            algorithms.AES(key), modes.CBC(iv), backend=default_backend()
        )

    def unpad(self, data: bytes) -> bytes:
        unpadLength = data[-1]
        if isinstance(unpadLength, int):  # pyright: ignore
            cmp = bytes([data[-unpadLength]] * unpadLength)
        else:
            raise AssertionError("unpadLength is not integer")
            # unpadLength = ord(unpadLength)
            # cmp = data[-unpadLength] * unpadLength
        if data[-unpadLength:] != cmp:
            raise ValueError("Data not properly padded \n %s" % data)

        return data[0:-unpadLength]

    def pad(self, s: bytes) -> bytes:
        return s + ((16 - len(s) % 16) * chr(16 - len(s) % 16)).encode()

    def encrypt(self, raw: bytes) -> bytes:
        rawPadded = self.pad(raw)
        encryptor = self.cipher.encryptor()
        try:
            return encryptor.update(rawPadded) + encryptor.finalize()
        except ValueError:
            raise

    def decrypt(self, enc: bytes) -> bytes:
        decryptor = self.cipher.decryptor()
        return self.unpad(decryptor.update(enc) + decryptor.finalize())
