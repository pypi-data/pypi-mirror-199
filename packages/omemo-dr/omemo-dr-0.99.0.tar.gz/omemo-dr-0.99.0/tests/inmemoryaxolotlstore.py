from omemo_dr.state.axolotlstore import AxolotlStore

from .inmemoryidentitykeystore import InMemoryIdentityKeyStore
from .inmemoryprekeystore import InMemoryPreKeyStore
from .inmemorysessionstore import InMemorySessionStore
from .inmemorysignedprekeystore import InMemorySignedPreKeyStore


class InMemoryAxolotlStore(AxolotlStore):
    def __init__(self):
        self.identityKeyStore = InMemoryIdentityKeyStore()
        self.preKeyStore = InMemoryPreKeyStore()
        self.signedPreKeyStore = InMemorySignedPreKeyStore()
        self.sessionStore = InMemorySessionStore()

    def getIdentityKeyPair(self):
        return self.identityKeyStore.getIdentityKeyPair()

    def getLocalRegistrationId(self):
        return self.identityKeyStore.getLocalRegistrationId()

    def saveIdentity(self, recipientId, identityKey):
        self.identityKeyStore.saveIdentity(recipientId, identityKey)

    def isTrustedIdentity(self, recipientId, identityKey):
        return self.identityKeyStore.isTrustedIdentity(recipientId, identityKey)

    def loadPreKey(self, preKeyId):
        return self.preKeyStore.loadPreKey(preKeyId)

    def storePreKey(self, preKeyId, preKeyRecord):
        self.preKeyStore.storePreKey(preKeyId, preKeyRecord)

    def containsPreKey(self, preKeyId):
        return self.preKeyStore.containsPreKey(preKeyId)

    def removePreKey(self, preKeyId):
        self.preKeyStore.removePreKey(preKeyId)

    def loadSession(self, recipientId, deviceId):
        return self.sessionStore.loadSession(recipientId, deviceId)

    def getSubDeviceSessions(self, recipientId: str) -> list[int]:
        return self.sessionStore.getSubDeviceSessions(recipientId)

    def storeSession(self, recipientId, deviceId, sessionRecord):
        self.sessionStore.storeSession(recipientId, deviceId, sessionRecord)

    def containsSession(self, recipientId, deviceId):
        return self.sessionStore.containsSession(recipientId, deviceId)

    def deleteSession(self, recipientId, deviceId):
        self.sessionStore.deleteSession(recipientId, deviceId)

    def deleteAllSessions(self, recipientId):
        self.sessionStore.deleteAllSessions(recipientId)

    def loadSignedPreKey(self, signedPreKeyId):
        return self.signedPreKeyStore.loadSignedPreKey(signedPreKeyId)

    def loadSignedPreKeys(self):
        return self.signedPreKeyStore.loadSignedPreKeys()

    def storeSignedPreKey(self, signedPreKeyId, signedPreKeyRecord):
        self.signedPreKeyStore.storeSignedPreKey(signedPreKeyId, signedPreKeyRecord)

    def containsSignedPreKey(self, signedPreKeyId):
        return self.signedPreKeyStore.containsSignedPreKey(signedPreKeyId)

    def removeSignedPreKey(self, signedPreKeyId):
        return self.signedPreKeyStore.containsSignedPreKey()
