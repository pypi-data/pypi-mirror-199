from omemo_dr.state.sessionrecord import SessionRecord
from omemo_dr.state.sessionstore import SessionStore


class InMemorySessionStore(SessionStore):
    def __init__(self):
        self.sessions: dict[tuple[str, int], bytes] = {}

    def loadSession(self, recipientId: str, deviceId: int) -> SessionRecord:
        if self.containsSession(recipientId, deviceId):
            return SessionRecord(serialized=self.sessions[(recipientId, deviceId)])
        else:
            return SessionRecord()

    def getSubDeviceSessions(self, recipientId: str) -> list[int]:
        deviceIds: list[int] = []
        for k in self.sessions.keys():
            if k[0] == recipientId:
                deviceIds.append(k[1])

        return deviceIds

    def storeSession(
        self, recipientId: str, deviceId: int, sessionRecord: SessionRecord
    ) -> None:
        self.sessions[(recipientId, deviceId)] = sessionRecord.serialize()

    def containsSession(self, recipientId: str, deviceId: int) -> bool:
        return (recipientId, deviceId) in self.sessions

    def deleteSession(self, recipientId: str, deviceId: int) -> None:
        del self.sessions[(recipientId, deviceId)]

    def deleteAllSessions(self, recipientId: str) -> None:
        for k in self.sessions.keys():
            if k[0] == recipientId:
                del self.sessions[k]
