from __future__ import annotations

from typing import Union

import os

from .. import curve
from ..exceptions import InvalidKeyException
from .djbec import CurvePublicKey
from .djbec import DjbECPrivateKey
from .djbec import EdPublicKey
from .eckeypair import ECKeyPair

CURVE25519_KEY_LEN = 33
ED25519_KEY_LEN = 32


class Curve:
    DJB_TYPE = 5

    @staticmethod
    def _generatePrivateKey() -> bytes:
        rand = os.urandom(32)
        return curve.generate_private_key(rand)

    @staticmethod
    def _generatePublicKey(privateKey: bytes) -> bytes:
        return curve.generate_public_key(privateKey)

    @staticmethod
    def generateKeyPair() -> ECKeyPair:
        privateKey = Curve._generatePrivateKey()
        publicKey = Curve._generatePublicKey(privateKey)
        return ECKeyPair(CurvePublicKey(publicKey), DjbECPrivateKey(privateKey))

    @staticmethod
    def decodePoint(
        _bytes: bytearray, offset: int = 0
    ) -> Union[CurvePublicKey, EdPublicKey]:
        key_type = _bytes[0]
        key_len = len(_bytes)

        if key_len == CURVE25519_KEY_LEN and key_type == Curve.DJB_TYPE:
            return CurvePublicKey(bytes(_bytes[1:]))

        elif key_len == ED25519_KEY_LEN:
            return EdPublicKey(_bytes)

        else:
            raise InvalidKeyException(
                "Unknown key type or length: %s - %s" % (key_type, key_len)
            )

    @staticmethod
    def decodePrivatePoint(_bytes: bytes) -> DjbECPrivateKey:
        return DjbECPrivateKey(bytes(_bytes))

    @staticmethod
    def calculateAgreement(
        publicKey: CurvePublicKey, privateKey: DjbECPrivateKey
    ) -> bytes:
        return curve.calculate_agreement(
            privateKey.getPrivateKey(), publicKey.get_bytes()
        )

    @staticmethod
    def verifySignature(
        ecPublicSigningKey: Union[CurvePublicKey, EdPublicKey],
        message: bytes,
        signature: bytes,
    ) -> bool:
        if isinstance(ecPublicSigningKey, CurvePublicKey):
            result = curve.verify_signature_curve(
                ecPublicSigningKey.get_bytes(), message, signature
            )
        else:
            result = curve.verify_signature_ed(
                ecPublicSigningKey.get_bytes(), message, signature
            )
        return result == 0

    @staticmethod
    def calculateSignature(privateSigningKey: DjbECPrivateKey, message: bytes) -> bytes:
        rand = os.urandom(64)
        return curve.calculate_signature(
            rand, privateSigningKey.getPrivateKey(), message
        )
