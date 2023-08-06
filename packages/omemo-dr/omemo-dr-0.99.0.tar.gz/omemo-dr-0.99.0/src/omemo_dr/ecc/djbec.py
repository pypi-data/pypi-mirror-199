from __future__ import annotations

from typing import Any

import binascii

from .. import curve
from ..util.byteutil import ByteUtil
from .ec import ECPrivateKey
from .ec import ECPublicKey

CURVE25519_KEY_LEN = 33
ED25519_KEY_LEN = 32
DJB_TYPE = 5


class DjbECPublicKey(ECPublicKey):
    def __init__(self, _bytes: bytes) -> None:
        self._publicKey = _bytes

    def getType(self) -> int:
        from .curve import Curve

        return Curve.DJB_TYPE

    def get_bytes(self) -> bytes:
        return self._publicKey

    def getPublicKey(self) -> bytes:
        return self._publicKey

    def __eq__(self, other: Any) -> bool:
        return self._publicKey == other.getPublicKey()

    def __lt__(self, other: Any) -> bool:
        myVal = int(binascii.hexlify(self._publicKey), 16)
        otherVal = int(binascii.hexlify(other.getPublicKey()), 16)

        return myVal < otherVal

    def __cmp__(self, other: Any) -> int:
        myVal = int(binascii.hexlify(self._publicKey), 16)
        otherVal = int(binascii.hexlify(other.getPublicKey()), 16)

        if myVal < otherVal:
            return -1
        elif myVal == otherVal:
            return 0
        else:
            return 1


class CurvePublicKey(DjbECPublicKey):
    def serialize(self) -> bytes:
        from .curve import Curve

        combined = ByteUtil.combine([Curve.DJB_TYPE], self._publicKey)
        return bytes(combined)

    def to_ed(self) -> EdPublicKey:
        return EdPublicKey(curve.convert_curve_to_ed_pubkey(self._publicKey))


class EdPublicKey(DjbECPublicKey):
    def to_curve(self) -> CurvePublicKey:
        return CurvePublicKey(curve.convert_ed_to_curve_pubkey(self._publicKey))

    def serialize(self) -> bytes:
        return self._publicKey


class DjbECPrivateKey(ECPrivateKey):
    def __init__(self, privateKey: bytes) -> None:
        self.privateKey = privateKey

    def getType(self) -> int:
        from .curve import Curve

        return Curve.DJB_TYPE

    def getPrivateKey(self) -> bytes:
        return self.privateKey

    def serialize(self) -> bytes:
        return self.privateKey

    def __eq__(self, other: Any) -> bool:
        return self.privateKey == other.getPrivateKey()
