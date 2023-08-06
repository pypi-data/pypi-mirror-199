from __future__ import annotations

from typing import cast
from typing import Optional

import google.protobuf.message

from . import storageprotos_pb2 as storageprotos
from .sessionstate import SessionState
from .sessionstate import SessionStructureProto


class SessionRecord:
    ARCHIVED_STATES_MAX_LENGTH = 40

    def __init__(
        self,
        sessionState: Optional[SessionState] = None,
        serialized: Optional[bytes] = None,
    ) -> None:
        self.previousStates: list[SessionState] = []
        if sessionState:
            self.sessionState = sessionState
            self.fresh = False

        elif serialized:
            record = cast(RecordStructureProto, storageprotos.RecordStructure())
            record.ParseFromString(serialized)
            self.sessionState = SessionState(record.currentSession)
            self.fresh = False
            for previousStructure in record.previousSessions:
                self.previousStates.append(SessionState(previousStructure))

        else:
            self.fresh = True
            self.sessionState = SessionState()

    def hasSessionState(self, version: int, aliceBaseKey: bytes) -> bool:
        if (
            self.sessionState.getSessionVersion() == version
            and aliceBaseKey == self.sessionState.getAliceBaseKey()
        ):
            return True

        for state in self.previousStates:
            if (
                state.getSessionVersion() == version
                and aliceBaseKey == state.getAliceBaseKey()
            ):
                return True

        return False

    def getSessionState(self) -> SessionState:
        return self.sessionState

    def getPreviousSessionStates(self) -> list[SessionState]:
        return self.previousStates

    def isFresh(self) -> bool:
        return self.fresh

    def archiveCurrentState(self) -> None:
        self.promoteState(SessionState())

    def promoteState(self, promotedState: SessionState) -> None:
        self.previousStates.insert(0, self.sessionState)
        self.sessionState = promotedState
        if len(self.previousStates) > self.__class__.ARCHIVED_STATES_MAX_LENGTH:
            self.previousStates.pop()

    def setState(self, sessionState: SessionState) -> None:
        self.sessionState = sessionState

    def serialize(self) -> bytes:
        previousStructures = [
            previousState.getStructure() for previousState in self.previousStates
        ]
        record = cast(RecordStructureProto, storageprotos.RecordStructure())
        record.currentSession.MergeFrom(self.sessionState.getStructure())
        record.previousSessions.extend(previousStructures)

        return record.SerializeToString()


class RecordStructureProto(google.protobuf.message.Message):
    currentSession: SessionStructureProto
    previousSessions: list[SessionStructureProto]
