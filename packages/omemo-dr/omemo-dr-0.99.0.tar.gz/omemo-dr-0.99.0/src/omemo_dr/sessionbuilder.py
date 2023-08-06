from __future__ import annotations

from typing import Optional

import logging

from .ecc.curve import Curve
from .exceptions import InvalidKeyException
from .exceptions import UntrustedIdentityException
from .protocol.prekeywhispermessage import PreKeyWhisperMessage
from .ratchet.aliceaxolotlparameters import AliceAxolotlParameters
from .ratchet.bobaxolotlparamaters import BobAxolotlParameters
from .ratchet.ratchetingsession import RatchetingSession
from .state.identitykeystore import IdentityKeyStore
from .state.prekeybundle import PreKeyBundle
from .state.prekeystore import PreKeyStore
from .state.sessionrecord import SessionRecord
from .state.sessionstore import SessionStore
from .state.signedprekeystore import SignedPreKeyStore
from .util.medium import Medium

logger = logging.getLogger(__name__)


class SessionBuilder:
    def __init__(
        self,
        sessionStore: SessionStore,
        preKeyStore: PreKeyStore,
        signedPreKeyStore: SignedPreKeyStore,
        identityKeyStore: IdentityKeyStore,
        recipientId: str,
        deviceId: int,
    ) -> None:
        self.sessionStore = sessionStore
        self.preKeyStore = preKeyStore
        self.signedPreKeyStore = signedPreKeyStore
        self.identityKeyStore = identityKeyStore
        self.recipientId = recipientId
        self.deviceId = deviceId

    def process(
        self, sessionRecord: SessionRecord, message: PreKeyWhisperMessage
    ) -> Optional[int]:
        messageVersion = message.getMessageVersion()
        theirIdentityKey = message.getIdentityKey()

        unsignedPreKeyId = None

        if not self.identityKeyStore.isTrustedIdentity(
            self.recipientId, theirIdentityKey
        ):
            raise UntrustedIdentityException(self.recipientId, theirIdentityKey)

        if messageVersion in (3, 4):
            unsignedPreKeyId = self.process_message(sessionRecord, message)
        else:
            raise AssertionError("Unknown version %s" % messageVersion)

        self.identityKeyStore.saveIdentity(self.recipientId, theirIdentityKey)

        return unsignedPreKeyId

    def process_message(
        self, sessionRecord: SessionRecord, message: PreKeyWhisperMessage
    ) -> Optional[int]:
        if sessionRecord.hasSessionState(
            message.getMessageVersion(), message.getBaseKey().serialize()
        ):
            logger.warn(
                "We've already setupgetMessageVersion a "
                "session for this V3 message, letting bundled "
                "message fall through..."
            )
            return None

        ourSignedPreKey = self.signedPreKeyStore.loadSignedPreKey(
            message.getSignedPreKeyId()
        )
        ourSignedPreKeyPair = ourSignedPreKey.getKeyPair()

        our_one_time_prekey = None
        if message.getPreKeyId() is not None:
            our_one_time_prekey = self.preKeyStore.loadPreKey(
                message.getPreKeyId()
            ).getKeyPair()

        parameters = BobAxolotlParameters(
            self.identityKeyStore.getIdentityKeyPair(),
            ourSignedPreKeyPair,
            ourSignedPreKeyPair,
            our_one_time_prekey,
            message.getIdentityKey(),
            message.getBaseKey(),
        )

        if not sessionRecord.isFresh():
            sessionRecord.archiveCurrentState()

        RatchetingSession.initializeSessionAsBob(
            sessionRecord.getSessionState(), message.getMessageVersion(), parameters
        )
        sessionRecord.getSessionState().setLocalRegistrationId(
            self.identityKeyStore.getLocalRegistrationId()
        )
        sessionRecord.getSessionState().setRemoteRegistrationId(
            message.getRegistrationId()
        )
        sessionRecord.getSessionState().setAliceBaseKey(
            message.getBaseKey().serialize()
        )

        if (
            message.getPreKeyId() is not None
            and message.getPreKeyId() != Medium.MAX_VALUE
        ):
            return message.getPreKeyId()
        else:
            return None

    def processPreKeyBundle(self, preKey: PreKeyBundle) -> None:
        if not self.identityKeyStore.isTrustedIdentity(
            self.recipientId, preKey.getIdentityKey()
        ):
            raise UntrustedIdentityException(self.recipientId, preKey.getIdentityKey())

        if preKey.getSignedPreKey() is not None and not Curve.verifySignature(
            preKey.getIdentityKey().getPublicKey(),
            preKey.getSignedPreKey().serialize(),
            preKey.getSignedPreKeySignature(),
        ):
            raise InvalidKeyException("Invalid signature on device key!")

        if preKey.getSignedPreKey() is None and preKey.getPreKey() is None:
            raise InvalidKeyException("Both signed and unsigned prekeys are absent!")

        sessionRecord = self.sessionStore.loadSession(self.recipientId, self.deviceId)
        ourBaseKey = Curve.generateKeyPair()
        theirSignedPreKey = preKey.getSignedPreKey()
        theirOneTimePreKey = preKey.getPreKey()
        theirOneTimePreKeyId = preKey.getPreKeyId()

        parameters = AliceAxolotlParameters(
            self.identityKeyStore.getIdentityKeyPair(),
            ourBaseKey,
            preKey.getIdentityKey(),
            theirSignedPreKey,
            theirSignedPreKey,
            theirOneTimePreKey,
        )

        if not sessionRecord.isFresh():
            sessionRecord.archiveCurrentState()

        RatchetingSession.initializeSessionAsAlice(
            sessionRecord.getSessionState(), preKey.getSessionVersion(), parameters
        )

        sessionRecord.getSessionState().setUnacknowledgedPreKeyMessage(
            theirOneTimePreKeyId, preKey.getSignedPreKeyId(), ourBaseKey.getPublicKey()
        )
        sessionRecord.getSessionState().setLocalRegistrationId(
            self.identityKeyStore.getLocalRegistrationId()
        )
        sessionRecord.getSessionState().setRemoteRegistrationId(
            preKey.getRegistrationId()
        )
        sessionRecord.getSessionState().setAliceBaseKey(
            ourBaseKey.getPublicKey().serialize()
        )
        self.sessionStore.storeSession(self.recipientId, self.deviceId, sessionRecord)
        self.identityKeyStore.saveIdentity(self.recipientId, preKey.getIdentityKey())
