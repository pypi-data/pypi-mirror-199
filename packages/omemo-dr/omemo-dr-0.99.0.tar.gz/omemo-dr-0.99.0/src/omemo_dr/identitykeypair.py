from __future__ import annotations

from typing import cast

import google.protobuf.message

from .ecc.curve import Curve
from .ecc.djbec import DjbECPrivateKey
from .identitykey import IdentityKey
from .state.storageprotos_pb2 import IdentityKeyPairStructure


class IdentityKeyPair:
    def __init__(self, structure: IdentityKeyPairStructureProto) -> None:
        self._structure = structure

    @classmethod
    def new(
        cls,
        identityKeyPublicKey: IdentityKey,
        ecPrivateKey: DjbECPrivateKey,
    ) -> IdentityKeyPair:
        structure = cast(IdentityKeyPairStructureProto, IdentityKeyPairStructure())

        structure.publicKey = identityKeyPublicKey.serialize()
        structure.privateKey = ecPrivateKey.serialize()

        return cls(structure)

    @classmethod
    def from_bytes(cls, serialized: bytes) -> IdentityKeyPair:
        structure = cast(IdentityKeyPairStructureProto, IdentityKeyPairStructure())
        structure.ParseFromString(serialized)
        return cls(structure)

    def getPublicKey(self) -> IdentityKey:
        return IdentityKey(bytearray(self._structure.publicKey), offset=0)

    def getPrivateKey(self) -> DjbECPrivateKey:
        return Curve.decodePrivatePoint(bytearray(self._structure.privateKey))

    def serialize(self) -> bytes:
        return self._structure.SerializeToString()


class IdentityKeyPairStructureProto(google.protobuf.message.Message):
    publicKey: bytes
    privateKey: bytes
