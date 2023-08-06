from __future__ import annotations

from typing import Optional

from ..ecc.ec import ECPublicKey
from ..ecc.eckeypair import ECKeyPair
from ..identitykey import IdentityKey
from ..identitykeypair import IdentityKeyPair


class BobAxolotlParameters:
    def __init__(
        self,
        ourIdentityKey: IdentityKeyPair,
        ourSignedPreKey: ECKeyPair,
        ourRatchetKey: ECKeyPair,
        ourOneTimePreKey: Optional[ECKeyPair],
        theirIdentityKey: IdentityKey,
        theirBaseKey: ECPublicKey,
    ) -> None:
        self.ourIdentityKey = ourIdentityKey
        self.ourSignedPreKey = ourSignedPreKey
        self.ourRatchetKey = ourRatchetKey
        self.ourOneTimePreKey = ourOneTimePreKey
        self.theirIdentityKey = theirIdentityKey
        self.theirBaseKey = theirBaseKey

        if (
            ourIdentityKey is None
            or ourSignedPreKey is None
            or ourRatchetKey is None
            or theirIdentityKey is None
            or theirBaseKey is None
        ):
            raise ValueError("Null value!")

    def getOurIdentityKey(self) -> IdentityKeyPair:
        return self.ourIdentityKey

    def getOurSignedPreKey(self) -> ECKeyPair:
        return self.ourSignedPreKey

    def getOurOneTimePreKey(self) -> Optional[ECKeyPair]:
        return self.ourOneTimePreKey

    def getTheirIdentityKey(self) -> IdentityKey:
        return self.theirIdentityKey

    def getTheirBaseKey(self) -> ECPublicKey:
        return self.theirBaseKey

    def getOurRatchetKey(self) -> ECKeyPair:
        return self.ourRatchetKey

    @staticmethod
    def newBuilder() -> Builder:
        return BobAxolotlParameters.Builder()

    class Builder:
        def __init__(self):
            self.ourIdentityKey = None
            self.ourSignedPreKey = None
            self.ourOneTimePreKey = None
            self.ourRatchetKey = None
            self.theirIdentityKey = None
            self.theirBaseKey = None

        def setOurIdentityKey(self, ourIdentityKey):
            self.ourIdentityKey = ourIdentityKey
            return self

        def setOurSignedPreKey(self, ourSignedPreKey):
            self.ourSignedPreKey = ourSignedPreKey
            return self

        def setOurOneTimePreKey(self, ourOneTimePreKey):
            self.ourOneTimePreKey = ourOneTimePreKey
            return self

        def setOurRatchetKey(self, ourRatchetKey):
            self.ourRatchetKey = ourRatchetKey
            return self

        def setTheirIdentityKey(self, theirIdentityKey):
            self.theirIdentityKey = theirIdentityKey
            return self

        def setTheirBaseKey(self, theirBaseKey):
            self.theirBaseKey = theirBaseKey
            return self

        def create(self):
            return BobAxolotlParameters(
                self.ourIdentityKey,
                self.ourSignedPreKey,
                self.ourRatchetKey,
                self.ourOneTimePreKey,
                self.theirIdentityKey,
                self.theirBaseKey,
            )
