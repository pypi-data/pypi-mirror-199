from __future__ import annotations

from ..ecc.curve import Curve
from ..ecc.djbec import CurvePublicKey
from ..ecc.eckeypair import ECKeyPair
from ..kdf.derivedrootsecrets import DerivedRootSecrets
from ..kdf.hkdf import HKDF
from .chainkey import ChainKey


class RootKey:
    def __init__(self, kdf: HKDF, key: bytes) -> None:
        self.kdf = kdf
        self.key = key

    def getKeyBytes(self) -> bytes:
        return self.key

    def createChain(
        self,
        ECPublicKey_theirRatchetKey: CurvePublicKey,
        ECKeyPair_ourRatchetKey: ECKeyPair,
    ) -> tuple[RootKey, ChainKey]:
        if self.kdf.sessionVersion <= 3:
            domain_separator = "WhisperRatchet"
        else:
            domain_separator = "OMEMO Root Chain"

        sharedSecret = Curve.calculateAgreement(
            ECPublicKey_theirRatchetKey, ECKeyPair_ourRatchetKey.getPrivateKey()
        )

        derivedSecretBytes = self.kdf.deriveSecrets(
            sharedSecret,
            domain_separator.encode(),
            DerivedRootSecrets.SIZE,
            salt=self.key,
        )

        derivedSecrets = DerivedRootSecrets(derivedSecretBytes)
        newRootKey = RootKey(self.kdf, derivedSecrets.getRootKey())
        newChainKey = ChainKey(self.kdf, derivedSecrets.getChainKey(), 0)
        return (newRootKey, newChainKey)
