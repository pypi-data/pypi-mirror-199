from __future__ import annotations

from typing import NoReturn
from typing import Optional
from typing import Union

from .ecc.curve import Curve
from .ecc.ec import ECPublicKey


class IdentityKey:
    def __init__(
        self,
        ecPubKeyOrBytes: Union[ECPublicKey, bytes, bytearray],
        offset: Optional[int] = None,
    ) -> None:
        if isinstance(ecPubKeyOrBytes, ECPublicKey):
            self.publicKey = ecPubKeyOrBytes
        else:
            assert offset is not None
            self.publicKey = Curve.decodePoint(bytearray(ecPubKeyOrBytes), offset)

    def getPublicKey(self) -> ECPublicKey:
        return self.publicKey

    def serialize(self) -> bytes:
        return self.publicKey.serialize()

    def get_fingerprint(self) -> NoReturn:
        raise Exception("IMPL ME")

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, IdentityKey)
        return self.publicKey == other.getPublicKey()

    def hashCode(self) -> NoReturn:
        raise Exception("IMPL ME")
