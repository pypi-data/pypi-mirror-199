from __future__ import annotations

from typing import cast

import google.protobuf.message
from google.protobuf.message import DecodeError

from ..ecc.curve import Curve
from ..ecc.ec import ECPublicKey
from ..exceptions import InvalidKeyException
from ..exceptions import InvalidMessageException
from ..exceptions import InvalidVersionException
from ..identitykey import IdentityKey
from ..util.byteutil import ByteUtil
from . import whisperprotos_pb2 as whisperprotos
from .ciphertextmessage import CiphertextMessage
from .whispermessage import WhisperMessage


class PreKeyWhisperMessage(CiphertextMessage):
    def __init__(
        self,
        serialized: bytes,
        messageVersion: int,
        registrationId: int,
        preKeyId: int,
        signedPreKeyId: int,
        ecPublicBaseKey: ECPublicKey,
        identityKey: IdentityKey,
        whisperMessage: WhisperMessage,
    ) -> None:
        self.serialized = serialized
        self.messageVersion = messageVersion
        self.registrationId = registrationId
        self.preKeyId = preKeyId
        self.signedPreKeyId = signedPreKeyId
        self.ecPublicBaseKey = ecPublicBaseKey
        self.identityKey = identityKey
        self.whisperMessage = whisperMessage

    @classmethod
    def new(
        cls,
        messageVersion: int,
        registrationId: int,
        preKeyId: int,
        signedPreKeyId: int,
        ecPublicBaseKey: ECPublicKey,
        identityKey: IdentityKey,
        whisperMessage: WhisperMessage,
    ) -> PreKeyWhisperMessage:
        prekey_message = cast(
            PreKeyWhisperMessageProto, whisperprotos.PreKeyWhisperMessage()
        )
        prekey_message.signedPreKeyId = signedPreKeyId
        prekey_message.preKeyId = preKeyId
        prekey_message.baseKey = ecPublicBaseKey.serialize()
        prekey_message.identityKey = identityKey.serialize()
        prekey_message.message = whisperMessage.serialize()
        prekey_message.registrationId = registrationId

        versionBytes = ByteUtil.intsToByteHighAndLow(3, 3)
        messageBytes = prekey_message.SerializeToString()

        serialized = bytes(ByteUtil.combine(versionBytes, messageBytes))

        return cls(
            serialized,
            messageVersion,
            registrationId,
            preKeyId,
            signedPreKeyId,
            ecPublicBaseKey,
            identityKey,
            whisperMessage,
        )

    @classmethod
    def from_bytes(cls, serialized: bytes) -> PreKeyWhisperMessage:
        try:
            version = ByteUtil.highBitsToInt(serialized[0])
            if version != 3:
                raise InvalidVersionException("Unknown version %s" % version)

            preKeyWhisperMessage = cast(
                PreKeyWhisperMessageProto, whisperprotos.PreKeyWhisperMessage()
            )
            preKeyWhisperMessage.ParseFromString(serialized[1:])

            if (
                preKeyWhisperMessage.signedPreKeyId is None
                or not preKeyWhisperMessage.baseKey
                or not preKeyWhisperMessage.identityKey
                or not preKeyWhisperMessage.message
            ):
                raise InvalidMessageException("Incomplete message")

            registrationId = preKeyWhisperMessage.registrationId
            preKeyId = preKeyWhisperMessage.preKeyId
            if preKeyWhisperMessage.signedPreKeyId is not None:
                signedPreKeyId = preKeyWhisperMessage.signedPreKeyId
            else:
                signedPreKeyId = -1

            baseKey = Curve.decodePoint(bytearray(preKeyWhisperMessage.baseKey), 0)

            identityKey = IdentityKey(
                Curve.decodePoint(bytearray(preKeyWhisperMessage.identityKey), 0)
            )
            message = WhisperMessage.from_bytes(preKeyWhisperMessage.message)
        except (InvalidKeyException, DecodeError) as error:
            raise InvalidMessageException(str(error))

        return cls(
            serialized,
            version,
            registrationId,
            preKeyId,
            signedPreKeyId,
            baseKey,
            identityKey,
            message,
        )

    def getMessageVersion(self) -> int:
        return self.messageVersion

    def getIdentityKey(self):
        return self.identityKey

    def getRegistrationId(self) -> int:
        return self.registrationId

    def getPreKeyId(self) -> int:
        return self.preKeyId

    def getSignedPreKeyId(self) -> int:
        return self.signedPreKeyId

    def getBaseKey(self) -> ECPublicKey:
        return self.ecPublicBaseKey

    def getWhisperMessage(self) -> WhisperMessage:
        return self.whisperMessage

    def serialize(self) -> bytes:
        return self.serialized

    def getType(self) -> int:
        return CiphertextMessage.PREKEY_TYPE


class PreKeyWhisperMessageProto(google.protobuf.message.Message):
    signedPreKeyId: int
    preKeyId: int
    baseKey: bytes
    identityKey: bytes
    message: bytes
    registrationId: int
