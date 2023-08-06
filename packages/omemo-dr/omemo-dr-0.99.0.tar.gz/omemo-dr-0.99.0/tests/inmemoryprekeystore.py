from omemo_dr.exceptions import InvalidKeyIdException
from omemo_dr.state.prekeyrecord import PreKeyRecord
from omemo_dr.state.prekeystore import PreKeyStore


class InMemoryPreKeyStore(PreKeyStore):
    def __init__(self) -> None:
        self.store: dict[int, bytes] = {}

    def loadPreKey(self, preKeyId) -> PreKeyRecord:
        if preKeyId not in self.store:
            raise InvalidKeyIdException("No such prekeyRecord!")

        return PreKeyRecord.from_bytes(self.store[preKeyId])

    def storePreKey(self, preKeyId: int, preKeyRecord: PreKeyRecord) -> None:
        self.store[preKeyId] = preKeyRecord.serialize()

    def containsPreKey(self, preKeyId: int) -> bool:
        return preKeyId in self.store

    def removePreKey(self, preKeyId: int) -> None:
        if preKeyId in self.store:
            del self.store[preKeyId]
