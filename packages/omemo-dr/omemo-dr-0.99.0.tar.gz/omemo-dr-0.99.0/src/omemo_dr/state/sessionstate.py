from __future__ import annotations

from typing import cast
from typing import Optional
from typing import Union

import google.protobuf.message

from ..ecc.curve import Curve
from ..ecc.djbec import CurvePublicKey
from ..ecc.ec import ECPublicKey
from ..ecc.eckeypair import ECKeyPair
from ..identitykeypair import IdentityKey
from ..identitykeypair import IdentityKeyPair
from ..kdf.hkdf import HKDF
from ..kdf.messagekeys import MessageKeys
from ..ratchet.chainkey import ChainKey
from ..ratchet.rootkey import RootKey
from . import storageprotos_pb2 as storageprotos


class SessionState:
    def __init__(
        self, session: Optional[Union[SessionState, SessionStructureProto]] = None
    ) -> None:
        if session is None:
            self.sessionStructure = cast(
                SessionStructureProto, storageprotos.SessionStructure()
            )

        elif isinstance(session, SessionState):
            self.sessionStructure = cast(
                SessionStructureProto, storageprotos.SessionStructure()
            )
            self.sessionStructure.CopyFrom(session.getStructure())

        else:
            self.sessionStructure = session

    def getStructure(self) -> SessionStructureProto:
        return self.sessionStructure

    def getAliceBaseKey(self) -> bytes:
        return self.sessionStructure.aliceBaseKey

    def setAliceBaseKey(self, aliceBaseKey: bytes) -> None:
        self.sessionStructure.aliceBaseKey = aliceBaseKey

    def setSessionVersion(self, version: int) -> None:
        self.sessionStructure.sessionVersion = version

    def getSessionVersion(self) -> int:
        sessionVersion = self.sessionStructure.sessionVersion
        return 2 if sessionVersion == 0 else sessionVersion

    def setRemoteIdentityKey(self, identityKey: IdentityKey) -> None:
        self.sessionStructure.remoteIdentityPublic = identityKey.serialize()

    def setLocalIdentityKey(self, identityKey: IdentityKey) -> None:
        self.sessionStructure.localIdentityPublic = identityKey.serialize()

    def getRemoteIdentityKey(self) -> IdentityKey:
        assert self.sessionStructure.remoteIdentityPublic is not None
        return IdentityKey(self.sessionStructure.remoteIdentityPublic, 0)

    def getLocalIdentityKey(self) -> IdentityKey:
        return IdentityKey(self.sessionStructure.localIdentityPublic, 0)

    def getPreviousCounter(self) -> int:
        return self.sessionStructure.previousCounter

    def setPreviousCounter(self, previousCounter: int) -> None:
        self.sessionStructure.previousCounter = previousCounter

    def getRootKey(self) -> RootKey:
        return RootKey(HKDF(self.getSessionVersion()), self.sessionStructure.rootKey)

    def setRootKey(self, rootKey: RootKey) -> None:
        self.sessionStructure.rootKey = rootKey.getKeyBytes()

    def getSenderRatchetKey(self) -> CurvePublicKey:
        key = Curve.decodePoint(
            bytearray(self.sessionStructure.senderChain.senderRatchetKey), 0
        )
        assert isinstance(key, CurvePublicKey)
        return key

    def getSenderRatchetKeyPair(self) -> ECKeyPair:
        publicKey = self.getSenderRatchetKey()
        privateKey = Curve.decodePrivatePoint(
            self.sessionStructure.senderChain.senderRatchetKeyPrivate
        )

        return ECKeyPair(publicKey, privateKey)

    def hasReceiverChain(self, ECPublickKey_senderEphemeral: CurvePublicKey) -> bool:
        return self.getReceiverChain(ECPublickKey_senderEphemeral) is not None

    def hasSenderChain(self) -> bool:
        return self.sessionStructure.HasField("senderChain")

    def getReceiverChain(
        self, ECPublickKey_senderEphemeral: CurvePublicKey
    ) -> Optional[tuple[ChainStructureProto, int]]:
        receiverChains = self.sessionStructure.receiverChains
        index = 0
        for receiverChain in receiverChains:
            chainSenderRatchetKey = Curve.decodePoint(
                bytearray(receiverChain.senderRatchetKey), 0
            )
            if chainSenderRatchetKey == ECPublickKey_senderEphemeral:
                return (receiverChain, index)

            index += 1

    def getReceiverChainKey(
        self, ECPublicKey_senderEphemeral: CurvePublicKey
    ) -> ChainKey:
        receiverChainAndIndex = self.getReceiverChain(ECPublicKey_senderEphemeral)
        assert receiverChainAndIndex is not None
        receiverChain = receiverChainAndIndex[0]
        assert receiverChain is not None

        return ChainKey(
            HKDF(self.getSessionVersion()),
            receiverChain.chainKey.key,
            receiverChain.chainKey.index,
        )

    def addReceiverChain(
        self, ECPublickKey_senderRatchetKey: CurvePublicKey, chainKey: ChainKey
    ) -> None:
        senderRatchetKey = ECPublickKey_senderRatchetKey

        chain = cast(
            ChainStructureProto, storageprotos.SessionStructure.Chain()
        )  # pyright: ignore
        chain.senderRatchetKey = senderRatchetKey.serialize()
        chain.chainKey.key = chainKey.getKey()
        chain.chainKey.index = chainKey.getIndex()

        self.sessionStructure.receiverChains.extend([chain])

        if len(self.sessionStructure.receiverChains) > 5:
            del self.sessionStructure.receiverChains[0]

    def setSenderChain(
        self, ECKeyPair_senderRatchetKeyPair: ECKeyPair, chainKey: ChainKey
    ) -> None:
        senderRatchetKeyPair = ECKeyPair_senderRatchetKeyPair

        self.sessionStructure.senderChain.senderRatchetKey = (
            senderRatchetKeyPair.getPublicKey().serialize()
        )
        self.sessionStructure.senderChain.senderRatchetKeyPrivate = (
            senderRatchetKeyPair.getPrivateKey().serialize()
        )
        self.sessionStructure.senderChain.chainKey.key = chainKey.key
        self.sessionStructure.senderChain.chainKey.index = chainKey.index

    def getSenderChainKey(self) -> ChainKey:
        chainKeyStructure = self.sessionStructure.senderChain.chainKey
        return ChainKey(
            HKDF(self.getSessionVersion()),
            chainKeyStructure.key,
            chainKeyStructure.index,
        )

    def setSenderChainKey(self, ChainKey_nextChainKey: ChainKey) -> None:
        nextChainKey = ChainKey_nextChainKey

        self.sessionStructure.senderChain.chainKey.key = nextChainKey.getKey()
        self.sessionStructure.senderChain.chainKey.index = nextChainKey.getIndex()

    def hasMessageKeys(
        self, ECPublickKey_senderEphemeral: CurvePublicKey, counter: int
    ) -> bool:
        senderEphemeral = ECPublickKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        assert chainAndIndex is not None
        chain = chainAndIndex[0]
        if chain is None:
            return False

        messageKeyList = chain.messageKeys
        for messageKey in messageKeyList:
            if messageKey.index == counter:
                return True

        return False

    def removeMessageKeys(
        self, ECPublicKey_senderEphemeral: CurvePublicKey, counter: int
    ) -> MessageKeys:
        senderEphemeral = ECPublicKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        assert chainAndIndex is not None
        chain = chainAndIndex[0]
        assert chain is not None

        messageKeyList = chain.messageKeys
        result = None

        for i in range(0, len(messageKeyList)):
            messageKey = messageKeyList[i]
            if messageKey.index == counter:
                result = MessageKeys(
                    messageKey.cipherKey,
                    messageKey.macKey,
                    messageKey.iv,
                    messageKey.index,
                )
                del messageKeyList[i]
                break

        assert result is not None

        self.sessionStructure.receiverChains[chainAndIndex[1]].CopyFrom(chain)

        return result

    def setMessageKeys(
        self, ECPublicKey_senderEphemeral: CurvePublicKey, messageKeys: MessageKeys
    ) -> None:
        senderEphemeral = ECPublicKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        assert chainAndIndex is not None
        chain = chainAndIndex[0]
        messageKeyStructure = chain.messageKeys.add()  # pyright: ignore
        messageKeyStructure.cipherKey = messageKeys.getCipherKey()
        messageKeyStructure.macKey = messageKeys.getMacKey()
        messageKeyStructure.index = messageKeys.getCounter()
        messageKeyStructure.iv = messageKeys.getIv()

        self.sessionStructure.receiverChains[chainAndIndex[1]].CopyFrom(chain)

    def setReceiverChainKey(
        self, ECPublicKey_senderEphemeral: CurvePublicKey, chainKey: ChainKey
    ) -> None:
        senderEphemeral = ECPublicKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        assert chainAndIndex is not None
        chain = chainAndIndex[0]
        chain.chainKey.key = chainKey.getKey()
        chain.chainKey.index = chainKey.getIndex()

        self.sessionStructure.receiverChains[chainAndIndex[1]].CopyFrom(chain)

    def setPendingKeyExchange(
        self,
        sequence: int,
        ourBaseKey: ECKeyPair,
        ourRatchetKey: ECKeyPair,
        ourIdentityKey: IdentityKeyPair,
    ) -> None:
        structure = cast(
            PendingKeyExchangeStructureProto, self.sessionStructure.PendingKeyExchange()
        )  # pyright: ignore
        structure.sequence = sequence
        structure.localBaseKey = ourBaseKey.getPublicKey().serialize()
        structure.localBaseKeyPrivate = ourBaseKey.getPrivateKey().serialize()
        structure.localRatchetKey = ourRatchetKey.getPublicKey().serialize()
        structure.localRatchetKeyPrivate = ourRatchetKey.getPrivateKey().serialize()
        structure.localIdentityKey = ourIdentityKey.getPublicKey().serialize()
        structure.localIdentityKeyPrivate = ourIdentityKey.getPrivateKey().serialize()

        self.sessionStructure.pendingKeyExchange.MergeFrom(structure)

    def getPendingKeyExchangeSequence(self) -> int:
        return self.sessionStructure.pendingKeyExchange.sequence

    def getPendingKeyExchangeBaseKey(self) -> ECKeyPair:
        publicKey = Curve.decodePoint(
            bytearray(self.sessionStructure.pendingKeyExchange.localBaseKey), 0
        )
        privateKey = Curve.decodePrivatePoint(
            self.sessionStructure.pendingKeyExchange.localBaseKeyPrivate
        )
        return ECKeyPair(publicKey, privateKey)

    def getPendingKeyExchangeRatchetKey(self) -> ECKeyPair:
        publicKey = Curve.decodePoint(
            bytearray(self.sessionStructure.pendingKeyExchange.localRatchetKey), 0
        )
        privateKey = Curve.decodePrivatePoint(
            self.sessionStructure.pendingKeyExchange.localRatchetKeyPrivate
        )
        return ECKeyPair(publicKey, privateKey)

    def getPendingKeyExchangeIdentityKey(self) -> IdentityKeyPair:
        publicKey = IdentityKey(
            bytearray(self.sessionStructure.pendingKeyExchange.localIdentityKey), 0
        )

        privateKey = Curve.decodePrivatePoint(
            self.sessionStructure.pendingKeyExchange.localIdentityKeyPrivate
        )
        return IdentityKeyPair.new(publicKey, privateKey)

    def hasPendingKeyExchange(self) -> bool:
        return self.sessionStructure.HasField("pendingKeyExchange")

    def setUnacknowledgedPreKeyMessage(
        self, preKeyId: int, signedPreKeyId: int, baseKey: CurvePublicKey
    ) -> None:
        self.sessionStructure.pendingPreKey.signedPreKeyId = signedPreKeyId
        self.sessionStructure.pendingPreKey.baseKey = baseKey.serialize()

        if preKeyId is not None:
            self.sessionStructure.pendingPreKey.preKeyId = preKeyId

    def hasUnacknowledgedPreKeyMessage(self) -> bool:
        return self.sessionStructure.HasField("pendingPreKey")

    def getUnacknowledgedPreKeyMessageItems(self) -> UnacknowledgedPreKeyMessageItems:
        preKeyId = None
        if self.sessionStructure.pendingPreKey.HasField("preKeyId"):
            preKeyId = self.sessionStructure.pendingPreKey.preKeyId

        assert preKeyId is not None
        return SessionState.UnacknowledgedPreKeyMessageItems(
            preKeyId,
            self.sessionStructure.pendingPreKey.signedPreKeyId,
            Curve.decodePoint(
                bytearray(self.sessionStructure.pendingPreKey.baseKey), 0
            ),
        )

    def clearUnacknowledgedPreKeyMessage(self) -> None:
        self.sessionStructure.ClearField("pendingPreKey")

    def setRemoteRegistrationId(self, registrationId: int) -> None:
        self.sessionStructure.remoteRegistrationId = registrationId

    def getRemoteRegistrationId(self) -> int:
        return self.sessionStructure.remoteRegistrationId

    def setLocalRegistrationId(self, registrationId: int) -> None:
        self.sessionStructure.localRegistrationId = registrationId

    def getLocalRegistrationId(self) -> int:
        return self.sessionStructure.localRegistrationId

    def serialize(self) -> bytes:
        return self.sessionStructure.SerializeToString()

    class UnacknowledgedPreKeyMessageItems:
        def __init__(
            self, preKeyId: int, signedPreKeyId: int, baseKey: ECPublicKey
        ) -> None:
            self.preKeyId = preKeyId
            self.signedPreKeyId = signedPreKeyId
            self.baseKey = baseKey

        def getPreKeyId(self) -> int:
            return self.preKeyId

        def getSignedPreKeyId(self) -> int:
            return self.signedPreKeyId

        def getBaseKey(self) -> ECPublicKey:
            return self.baseKey


class MessageKeyStructureProto(google.protobuf.message.Message):
    index: int
    cipherKey: bytes
    macKey: bytes
    iv: bytes


class ChainKeyStructureProto(google.protobuf.message.Message):
    index: int
    key: bytes


class ChainStructureProto(google.protobuf.message.Message):
    senderRatchetKey: bytes
    senderRatchetKeyPrivate: bytes
    chainKey: ChainKeyStructureProto
    messageKeys: list[MessageKeyStructureProto]


class PendingKeyExchangeStructureProto(google.protobuf.message.Message):
    sequence: int
    localBaseKey: bytes
    localBaseKeyPrivate: bytes
    localRatchetKey: bytes
    localRatchetKeyPrivate: bytes
    localIdentityKey: bytes
    localIdentityKeyPrivate: bytes


class PendingPreKeyStructureProto(google.protobuf.message.Message):
    preKeyId: int
    signedPreKeyId: int
    baseKey: bytes


class SessionStructureProto(google.protobuf.message.Message):
    sessionVersion: int
    localIdentityPublic: bytes
    remoteIdentityPublic: bytes
    rootKey: bytes
    previousCounter: int
    senderChain: ChainStructureProto
    receiverChains: list[ChainStructureProto]
    pendingKeyExchange: PendingKeyExchangeStructureProto
    pendingPreKey: PendingPreKeyStructureProto
    remoteRegistrationId: int
    localRegistrationId: int
    needsRefresh: bool
    aliceBaseKey: bytes
