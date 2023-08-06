from __future__ import annotations

from .djbec import DjbECPrivateKey
from .ec import ECPublicKey


class ECKeyPair:
    def __init__(self, publicKey: ECPublicKey, privateKey: DjbECPrivateKey) -> None:
        self.publicKey = publicKey
        self.privateKey = privateKey

    def getPrivateKey(self) -> DjbECPrivateKey:
        return self.privateKey

    def getPublicKey(self) -> ECPublicKey:
        return self.publicKey
