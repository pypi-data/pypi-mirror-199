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
from . import omemo_pb2 as omemoprotos
from .ciphertextmessage import CiphertextMessage


class OMEMOMessage(CiphertextMessage):
    MAC_LENGTH = 16

    def __init__(
        self,
        serialized: bytes,
        senderRatchetKey: CurvePublicKey,
        counter: int,
        previousCounter: int,
        ciphertext: bytes,
    ):
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
    ) -> OMEMOMessage:
        omemo_message = cast(OMEMOMessageProto, omemoprotos.OMEMOMessage())

        omemo_message.dh_pub = ECPublicKey_senderRatchetKey.serialize()
        omemo_message.n = counter
        omemo_message.pn = previousCounter
        omemo_message.ciphertext = ciphertext
        omemo_message = omemo_message.SerializeToString()

        mac = cls.getMac(senderIdentityKey, receiverIdentityKey, macKey, omemo_message)

        authenticated_message = cast(
            OMEMOAuthenticatedMessageProto, omemoprotos.OMEMOAuthenticatedMessage()
        )
        authenticated_message.mac = mac
        authenticated_message.message = omemo_message
        authenticated_message = authenticated_message.SerializeToString()

        return cls(
            authenticated_message,
            ECPublicKey_senderRatchetKey,
            counter,
            previousCounter,
            ciphertext,
        )

    @classmethod
    def from_bytes(cls, serialized: bytes) -> OMEMOMessage:
        authenticated_message = cast(
            OMEMOAuthenticatedMessageProto, omemoprotos.OMEMOAuthenticatedMessage()
        )
        try:
            authenticated_message.ParseFromString(serialized)
        except google.protobuf.message.DecodeError as error:
            raise InvalidMessageException(str(error))

        omemo_message = cast(OMEMOMessageProto, omemoprotos.OMEMOMessage())

        try:
            omemo_message.ParseFromString(authenticated_message.message)
        except google.protobuf.message.DecodeError as error:
            raise InvalidMessageException(str(error))

        try:
            senderRatchetKey = Curve.decodePoint(bytearray(omemo_message.dh_pub), 0)
            assert isinstance(senderRatchetKey, CurvePublicKey)
        except InvalidKeyException as error:
            raise InvalidMessageException(str(error))

        return OMEMOMessage(
            serialized,
            senderRatchetKey,
            omemo_message.n,
            omemo_message.pn,
            omemo_message.ciphertext,
        )

    def getSenderRatchetKey(self) -> CurvePublicKey:
        return self.senderRatchetKey

    def getMessageVersion(self) -> int:
        return 4

    def getCounter(self) -> int:
        return self.counter

    def getBody(self) -> bytes:
        return self.ciphertext

    def verifyMac(
        self,
        senderIdentityKey: IdentityKey,
        receiverIdentityKey: IdentityKey,
        macKey: bytes,
    ):
        parts = ByteUtil.split(
            self.serialized,
            len(self.serialized) - self.__class__.MAC_LENGTH,
            self.__class__.MAC_LENGTH,
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
        mac.update(bytes(serialized))
        fullMac = mac.digest()
        return ByteUtil.trim(fullMac, cls.MAC_LENGTH)

    def serialize(self) -> bytes:
        return self.serialized

    def getType(self) -> int:
        return CiphertextMessage.WHISPER_TYPE


class OMEMOMessageProto(google.protobuf.message.Message):
    n: int
    pn: int
    dh_pub: bytes
    ciphertext: bytes


class OMEMOAuthenticatedMessageProto(google.protobuf.message.Message):
    mac: bytes
    message: bytes
