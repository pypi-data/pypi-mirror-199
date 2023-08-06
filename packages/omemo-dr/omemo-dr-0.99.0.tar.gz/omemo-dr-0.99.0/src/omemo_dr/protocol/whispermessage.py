from __future__ import annotations

from typing import cast

import hashlib
import hmac

import google.protobuf.message

from ..ecc.curve import Curve
from ..ecc.djbec import CurvePublicKey
from ..exceptions import InvalidKeyException
from ..exceptions import InvalidMessageException
from ..identitykey import IdentityKey
from ..util.byteutil import ByteUtil
from . import whisperprotos_pb2 as whisperprotos
from .ciphertextmessage import CiphertextMessage


class WhisperMessage(CiphertextMessage):
    MAC_LENGTH = 8

    def __init__(
        self,
        serialized: bytes,
        senderRatchetKey: CurvePublicKey,
        counter: int,
        previousCounter: int,
        ciphertext: bytes,
    ) -> None:
        self.serialized = serialized
        self.senderRatchetKey = senderRatchetKey
        self.counter = counter
        self.previousCounter = previousCounter
        self.ciphertext = ciphertext

    @classmethod
    def new(
        cls,
        messageVersion: int,
        macKey: bytes,
        ECPublicKey_senderRatchetKey: CurvePublicKey,
        counter: int,
        previousCounter: int,
        ciphertext: bytes,
        senderIdentityKey: IdentityKey,
        receiverIdentityKey: IdentityKey,
    ) -> WhisperMessage:
        version = ByteUtil.intsToByteHighAndLow(messageVersion, messageVersion)

        message = cast(WhisperMessageProto, whisperprotos.WhisperMessage())
        message.ratchetKey = ECPublicKey_senderRatchetKey.serialize()
        message.counter = counter
        message.previousCounter = previousCounter
        message.ciphertext = ciphertext
        message = message.SerializeToString()

        mac = cls.getMac(
            senderIdentityKey,
            receiverIdentityKey,
            macKey,
            ByteUtil.combine(version, message),
        )

        serialized = bytes(ByteUtil.combine(version, message, mac))

        return cls(
            serialized,
            ECPublicKey_senderRatchetKey,
            counter,
            previousCounter,
            ciphertext,
        )

    @classmethod
    def from_bytes(cls, serialized: bytes) -> WhisperMessage:
        messageParts = ByteUtil.split(
            serialized,
            1,
            len(serialized) - 1 - WhisperMessage.MAC_LENGTH,
            WhisperMessage.MAC_LENGTH,
        )

        version = ByteUtil.highBitsToInt(messageParts[0][0])
        message = messageParts[1]
        _mac = messageParts[2]

        if version != 3:
            raise InvalidMessageException("Unknown version: %s" % version)

        whisperMessage = cast(WhisperMessageProto, whisperprotos.WhisperMessage())
        whisperMessage.ParseFromString(message)

        if not whisperMessage.ciphertext or not whisperMessage.ratchetKey:
            raise InvalidMessageException("Incomplete message")

        try:
            senderRatchetKey = Curve.decodePoint(
                bytearray(whisperMessage.ratchetKey), 0
            )
            assert isinstance(senderRatchetKey, CurvePublicKey)
        except InvalidKeyException as e:
            raise InvalidMessageException(str(e))

        return WhisperMessage(
            serialized,
            senderRatchetKey,
            whisperMessage.counter,
            whisperMessage.previousCounter,
            whisperMessage.ciphertext,
        )

    def getSenderRatchetKey(self) -> CurvePublicKey:
        return self.senderRatchetKey

    def getMessageVersion(self) -> int:
        return 3

    def getCounter(self) -> int:
        return self.counter

    def getBody(self) -> bytes:
        return self.ciphertext

    def verifyMac(
        self,
        senderIdentityKey: IdentityKey,
        receiverIdentityKey: IdentityKey,
        macKey: bytes,
    ) -> None:
        parts = ByteUtil.split(
            self.serialized, len(self.serialized) - self.MAC_LENGTH, self.MAC_LENGTH
        )
        ourMac = self.getMac(senderIdentityKey, receiverIdentityKey, macKey, parts[0])
        theirMac = parts[1]

        if ourMac != theirMac:
            raise InvalidMessageException("Bad Mac!")

    @classmethod
    def getMac(
        cls,
        senderIdentityKey: IdentityKey,
        receiverIdentityKey: IdentityKey,
        macKey: bytes,
        serialized: bytes,
    ) -> bytes:
        mac = hmac.new(macKey, digestmod=hashlib.sha256)
        mac.update(senderIdentityKey.getPublicKey().serialize())
        mac.update(receiverIdentityKey.getPublicKey().serialize())
        mac.update(serialized)
        fullMac = mac.digest()
        return ByteUtil.trim(fullMac, cls.MAC_LENGTH)

    def serialize(self) -> bytes:
        return self.serialized

    def getType(self) -> int:
        return CiphertextMessage.WHISPER_TYPE


class WhisperMessageProto(google.protobuf.message.Message):
    ratchetKey: bytes
    counter: int
    previousCounter: int
    ciphertext: bytes
