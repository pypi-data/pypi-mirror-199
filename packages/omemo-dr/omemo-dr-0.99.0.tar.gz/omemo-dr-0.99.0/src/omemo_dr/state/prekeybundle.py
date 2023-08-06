from __future__ import annotations

from ..ecc.djbec import CurvePublicKey
from ..ecc.djbec import EdPublicKey
from ..ecc.ec import ECPublicKey
from ..identitykey import IdentityKey


class PreKeyBundle:
    def __init__(
        self,
        registrationId: int,
        deviceId: int,
        preKeyId: int,
        ECPublicKey_preKeyPublic: ECPublicKey,
        signedPreKeyId: int,
        ECPublicKey_signedPreKeyPublic: ECPublicKey,
        signedPreKeySignature: bytes,
        identityKey: IdentityKey,
    ) -> None:
        self.registrationId = registrationId
        self.deviceId = deviceId
        self.preKeyId = preKeyId
        self.preKeyPublic = ECPublicKey_preKeyPublic
        self.signedPreKeyId = signedPreKeyId
        self.signedPreKeyPublic = ECPublicKey_signedPreKeyPublic
        self.signedPreKeySignature = signedPreKeySignature
        self.identityKey = identityKey

    def getDeviceId(self) -> int:
        return self.deviceId

    def getPreKeyId(self) -> int:
        return self.preKeyId

    def getPreKey(self) -> ECPublicKey:
        return self.preKeyPublic

    def getSignedPreKeyId(self) -> int:
        return self.signedPreKeyId

    def getSignedPreKey(self) -> ECPublicKey:
        return self.signedPreKeyPublic

    def getSignedPreKeySignature(self) -> bytes:
        return self.signedPreKeySignature

    def getIdentityKey(self) -> IdentityKey:
        return self.identityKey

    def getRegistrationId(self) -> int:
        return self.registrationId

    def getSessionVersion(self) -> int:
        publicKey = self.identityKey.getPublicKey()
        if isinstance(publicKey, CurvePublicKey):
            return 3

        elif isinstance(publicKey, EdPublicKey):
            return 4

        else:
            breakpoint()
            raise AssertionError("Unknown session version")
