from omemo_dr.exceptions import InvalidKeyIdException
from omemo_dr.state.signedprekeyrecord import SignedPreKeyRecord
from omemo_dr.state.signedprekeystore import SignedPreKeyStore


class InMemorySignedPreKeyStore(SignedPreKeyStore):
    def __init__(self):
        self.store = {}

    def loadSignedPreKey(self, signedPreKeyId):
        if signedPreKeyId not in self.store:
            raise InvalidKeyIdException(
                "No such signedprekeyrecord! %s " % signedPreKeyId
            )

        return SignedPreKeyRecord.from_bytes(self.store[signedPreKeyId])

    def loadSignedPreKeys(self):
        results = []
        for serialized in self.store.values():
            results.append(SignedPreKeyRecord.from_bytes(serialized))

        return results

    def storeSignedPreKey(self, signedPreKeyId, signedPreKeyRecord):
        self.store[signedPreKeyId] = signedPreKeyRecord.serialize()

    def containsSignedPreKey(self, signedPreKeyId):
        return signedPreKeyId in self.store

    def removeSignedPreKey(self, signedPreKeyId):
        del self.store[signedPreKeyId]
