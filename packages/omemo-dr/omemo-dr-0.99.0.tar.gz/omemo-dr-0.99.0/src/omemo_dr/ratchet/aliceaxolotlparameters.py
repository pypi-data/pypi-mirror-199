from __future__ import annotations

from ..ecc.ec import ECPublicKey
from ..ecc.eckeypair import ECKeyPair
from ..identitykey import IdentityKey
from ..identitykeypair import IdentityKeyPair


class AliceAxolotlParameters:
    def __init__(
        self,
        ourIdentityKey: IdentityKeyPair,
        ourBaseKey: ECKeyPair,
        theirIdentityKey: IdentityKey,
        theirSignedPreKey: ECPublicKey,
        theirRatchetKey: ECPublicKey,
        theirOneTimePreKey: ECPublicKey,
    ) -> None:
        self.ourBaseKey = ourBaseKey
        self.ourIdentityKey = ourIdentityKey
        self.theirSignedPreKey = theirSignedPreKey
        self.theirRatchetKey = theirRatchetKey
        self.theirIdentityKey = theirIdentityKey
        self.theirOneTimePreKey = theirOneTimePreKey

        if (
            ourBaseKey is None
            or ourIdentityKey is None
            or theirSignedPreKey is None
            or theirRatchetKey is None
            or theirIdentityKey is None
            or theirSignedPreKey is None
        ):
            raise ValueError("Null value!")

    def getOurIdentityKey(self) -> IdentityKeyPair:
        return self.ourIdentityKey

    def getOurBaseKey(self) -> ECKeyPair:
        return self.ourBaseKey

    def getTheirIdentityKey(self) -> IdentityKey:
        return self.theirIdentityKey

    def getTheirSignedPreKey(self) -> ECPublicKey:
        return self.theirSignedPreKey

    def getTheirOneTimePreKey(self) -> ECPublicKey:
        return self.theirOneTimePreKey

    def getTheirRatchetKey(self) -> ECPublicKey:
        return self.theirRatchetKey

    @staticmethod
    def newBuilder() -> AliceAxolotlParameters.Builder:
        return AliceAxolotlParameters.Builder()

    class Builder:
        def __init__(self):
            self.ourIdentityKey = None
            self.ourBaseKey = None
            self.theirIdentityKey = None
            self.theirSignedPreKey = None
            self.theirRatchetKey = None
            self.theirOneTimePreKey = None

        def setOurIdentityKey(
            self, ourIdentityKey: IdentityKeyPair
        ) -> AliceAxolotlParameters.Builder:
            self.ourIdentityKey = ourIdentityKey
            return self

        def setOurBaseKey(self, ourBaseKey: ECKeyPair):
            self.ourBaseKey = ourBaseKey
            return self

        def setTheirRatchetKey(self, theirRatchetKey: ECKeyPair):
            self.theirRatchetKey = theirRatchetKey
            return self

        def setTheirIdentityKey(self, theirIdentityKey):
            self.theirIdentityKey = theirIdentityKey
            return self

        def setTheirSignedPreKey(self, theirSignedPreKey):
            self.theirSignedPreKey = theirSignedPreKey
            return self

        def setTheirOneTimePreKey(self, theirOneTimePreKey: ECPublicKey):
            self.theirOneTimePreKey = theirOneTimePreKey
            return self

        def create(self):
            return AliceAxolotlParameters(
                self.ourIdentityKey,
                self.ourBaseKey,
                self.theirIdentityKey,
                self.theirSignedPreKey,
                self.theirRatchetKey,
                self.theirOneTimePreKey,
            )
