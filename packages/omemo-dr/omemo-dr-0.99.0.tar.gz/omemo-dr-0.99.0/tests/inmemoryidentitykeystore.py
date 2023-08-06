from omemo_dr.ecc.curve import Curve
from omemo_dr.identitykey import IdentityKey
from omemo_dr.identitykeypair import IdentityKeyPair
from omemo_dr.state.identitykeystore import IdentityKeyStore
from omemo_dr.util.keyhelper import KeyHelper


class InMemoryIdentityKeyStore(IdentityKeyStore):
    def __init__(self):
        self.trustedKeys = {}
        identityKeyPairKeys = Curve.generateKeyPair()
        self.identityKeyPair = IdentityKeyPair.new(
            IdentityKey(identityKeyPairKeys.getPublicKey()),
            identityKeyPairKeys.getPrivateKey(),
        )
        self.localRegistrationId = KeyHelper.generateRegistrationId()

    def getIdentityKeyPair(self):
        return self.identityKeyPair

    def getLocalRegistrationId(self):
        return self.localRegistrationId

    def saveIdentity(self, recipientId, identityKey):
        self.trustedKeys[recipientId] = identityKey

    def isTrustedIdentity(self, recipientId, identityKey):
        if recipientId not in self.trustedKeys:
            return True
        return self.trustedKeys[recipientId] == identityKey
