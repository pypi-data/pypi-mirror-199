from __future__ import annotations

import abc

from ..state.prekeyrecord import PreKeyRecord


class PreKeyStore(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def loadPreKey(self, preKeyId: int) -> PreKeyRecord:
        pass

    @abc.abstractmethod
    def storePreKey(self, preKeyId: int, preKeyRecord: PreKeyRecord):
        pass

    @abc.abstractmethod
    def containsPreKey(self, preKeyId: int) -> bool:
        pass

    @abc.abstractmethod
    def removePreKey(self, preKeyId: int) -> None:
        pass
