from __future__ import annotations

from typing import cast

import google.protobuf.message

from ..ecc.curve import Curve
from ..ecc.eckeypair import ECKeyPair
from .storageprotos_pb2 import PreKeyRecordStructure


class PreKeyRecord:
    def __init__(self, structure: PreKeyRecordStructureProto) -> None:
        self._structure = structure

    @classmethod
    def new(
        cls,
        _id: int,
        ecKeyPair: ECKeyPair,
    ) -> PreKeyRecord:
        structure = cast(PreKeyRecordStructureProto, PreKeyRecordStructure())
        structure.id = _id
        structure.publicKey = ecKeyPair.getPublicKey().serialize()
        structure.privateKey = ecKeyPair.getPrivateKey().serialize()
        return cls(structure)

    @classmethod
    def from_bytes(cls, serialized: bytes) -> PreKeyRecord:
        record = cast(PreKeyRecordStructureProto, PreKeyRecordStructure())
        record.ParseFromString(serialized)
        return cls(record)

    def getId(self) -> int:
        return self._structure.id

    def getKeyPair(self):
        publicKey = Curve.decodePoint(bytearray(self._structure.publicKey), 0)
        privateKey = Curve.decodePrivatePoint(bytearray(self._structure.privateKey))
        return ECKeyPair(publicKey, privateKey)

    def serialize(self) -> bytes:
        return self._structure.SerializeToString()


class PreKeyRecordStructureProto(google.protobuf.message.Message):
    id: int
    publicKey: bytes
    privateKey: bytes
