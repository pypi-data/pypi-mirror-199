from __future__ import annotations

import abc

from .signedprekeyrecord import SignedPreKeyRecord


class SignedPreKeyStore(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def loadSignedPreKey(self, signedPreKeyId: int) -> SignedPreKeyRecord:
        pass

    @abc.abstractmethod
    def loadSignedPreKeys(self) -> list[SignedPreKeyRecord]:
        pass

    @abc.abstractmethod
    def storeSignedPreKey(
        self, signedPreKeyId: int, signedPreKeyRecord: SignedPreKeyRecord
    ) -> None:
        pass

    @abc.abstractmethod
    def containsSignedPreKey(self, signedPreKeyId: int) -> bool:
        pass

    @abc.abstractmethod
    def removeSignedPreKey(self, signedPreKeyId: int) -> None:
        pass
