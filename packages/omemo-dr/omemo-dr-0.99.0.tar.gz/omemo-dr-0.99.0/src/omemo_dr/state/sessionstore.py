from __future__ import annotations

import abc

from .sessionrecord import SessionRecord


class SessionStore(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def loadSession(self, recipientId: str, deviceId: int) -> SessionRecord:
        pass

    @abc.abstractmethod
    def getSubDeviceSessions(self, recipientId: str) -> list[int]:
        pass

    @abc.abstractmethod
    def storeSession(
        self, recipientId: str, deviceId: int, sessionRecord: SessionRecord
    ) -> None:
        pass

    @abc.abstractmethod
    def containsSession(self, recipientId: str, deviceId: int) -> bool:
        pass

    @abc.abstractmethod
    def deleteSession(self, recipientId: str, deviceId: int) -> None:
        pass

    @abc.abstractmethod
    def deleteAllSessions(self, recipientId: str) -> None:
        pass
