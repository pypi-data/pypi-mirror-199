from __future__ import annotations

import abc

from ..identitykey import IdentityKey
from ..identitykeypair import IdentityKeyPair


class IdentityKeyStore(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getIdentityKeyPair(self) -> IdentityKeyPair:
        pass

    @abc.abstractmethod
    def getLocalRegistrationId(self) -> int:
        pass

    @abc.abstractmethod
    def saveIdentity(self, recipientId: str, identityKey: IdentityKey) -> None:
        pass

    @abc.abstractmethod
    def isTrustedIdentity(self, recipientId: str, identityKey: IdentityKey) -> bool:
        pass
