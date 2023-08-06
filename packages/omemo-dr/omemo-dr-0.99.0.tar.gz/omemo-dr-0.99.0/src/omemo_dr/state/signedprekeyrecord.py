from __future__ import annotations

from typing import cast

import google.protobuf.message

from ..ecc.curve import Curve
from ..ecc.eckeypair import ECKeyPair
from .storageprotos_pb2 import SignedPreKeyRecordStructure


class SignedPreKeyRecord:
    def __init__(self, structure: SignedPreKeyRecordStructureProto) -> None:
        self._structure = structure

    @classmethod
    def new(
        cls, _id: int, timestamp: int, ecKeyPair: ECKeyPair, signature: bytes
    ) -> SignedPreKeyRecord:
        record = cast(SignedPreKeyRecordStructureProto, SignedPreKeyRecordStructure())

        record.id = _id
        record.publicKey = ecKeyPair.getPublicKey().serialize()
        record.privateKey = ecKeyPair.getPrivateKey().serialize()
        record.signature = signature
        record.timestamp = timestamp

        return cls(record)

    @classmethod
    def from_bytes(cls, serialized: bytes) -> SignedPreKeyRecord:
        record = cast(SignedPreKeyRecordStructureProto, SignedPreKeyRecordStructure())
        record.ParseFromString(serialized)
        return cls(record)

    def getId(self) -> int:
        return self._structure.id

    def getTimestamp(self) -> int:
        return self._structure.timestamp

    def getKeyPair(self) -> ECKeyPair:
        publicKey = Curve.decodePoint(bytearray(self._structure.publicKey), 0)
        privateKey = Curve.decodePrivatePoint(bytearray(self._structure.privateKey))

        return ECKeyPair(publicKey, privateKey)

    def getSignature(self) -> bytes:
        return self._structure.signature

    def serialize(self) -> bytes:
        return self._structure.SerializeToString()


class SignedPreKeyRecordStructureProto(google.protobuf.message.Message):
    id: int
    publicKey: bytes
    privateKey: bytes
    signature: bytes
    timestamp: int
