import time
import unittest

from omemo_dr.ecc.curve import Curve
from omemo_dr.exceptions import InvalidKeyException
from omemo_dr.protocol.ciphertextmessage import CiphertextMessage
from omemo_dr.protocol.prekeywhispermessage import PreKeyWhisperMessage
from omemo_dr.protocol.whispermessage import WhisperMessage
from omemo_dr.sessionbuilder import SessionBuilder
from omemo_dr.sessioncipher import SessionCipher
from omemo_dr.state.prekeybundle import PreKeyBundle
from omemo_dr.state.prekeyrecord import PreKeyRecord
from omemo_dr.state.signedprekeyrecord import SignedPreKeyRecord

from .inmemoryaxolotlstore import InMemoryAxolotlStore
from .inmemoryidentitykeystore import InMemoryIdentityKeyStore


class SessionBuilderTest(unittest.TestCase):
    ALICE_RECIPIENT_ID = 5
    BOB_RECIPIENT_ID = 2

    def test_basicPreKeyV3(self):
        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(
            aliceStore,
            aliceStore,
            aliceStore,
            aliceStore,
            self.__class__.BOB_RECIPIENT_ID,
            1,
        )

        bobStore = InMemoryAxolotlStore()
        bobPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeySignature = Curve.calculateSignature(
            bobStore.getIdentityKeyPair().getPrivateKey(),
            bobSignedPreKeyPair.getPublicKey().serialize(),
        )

        bobPreKey = PreKeyBundle(
            bobStore.getLocalRegistrationId(),
            1,
            31337,
            bobPreKeyPair.getPublicKey(),
            22,
            bobSignedPreKeyPair.getPublicKey(),
            bobSignedPreKeySignature,
            bobStore.getIdentityKeyPair().getPublicKey(),
        )

        aliceSessionBuilder.processPreKeyBundle(bobPreKey)
        self.assertTrue(aliceStore.containsSession(self.__class__.BOB_RECIPIENT_ID, 1))
        self.assertTrue(
            aliceStore.loadSession(self.__class__.BOB_RECIPIENT_ID, 1)
            .getSessionState()
            .getSessionVersion()
            == 3
        )

        originalMessage = "L'homme est condamné à être libre"
        aliceSessionCipher = SessionCipher(
            aliceStore,
            aliceStore,
            aliceStore,
            aliceStore,
            self.__class__.BOB_RECIPIENT_ID,
            1,
        )
        outgoingMessage = aliceSessionCipher.encrypt(originalMessage)

        self.assertTrue(outgoingMessage.getType() == CiphertextMessage.PREKEY_TYPE)

        incomingMessage = PreKeyWhisperMessage.from_bytes(outgoingMessage.serialize())
        bobStore.storePreKey(
            31337, PreKeyRecord.new(bobPreKey.getPreKeyId(), bobPreKeyPair)
        )
        bobStore.storeSignedPreKey(
            22,
            SignedPreKeyRecord.new(
                22,
                int(time.time() * 1000),
                bobSignedPreKeyPair,
                bobSignedPreKeySignature,
            ),
        )

        bobSessionCipher = SessionCipher(
            bobStore, bobStore, bobStore, bobStore, self.__class__.ALICE_RECIPIENT_ID, 1
        )

        plaintext = bobSessionCipher.decryptPkmsg(incomingMessage)
        plaintext = plaintext.decode()
        self.assertEqual(originalMessage, plaintext)
        # @@TODO: in callback assertion
        # self.assertFalse(bobStore.containsSession(self.__class__.ALICE_RECIPIENT_ID, 1))

        self.assertTrue(bobStore.containsSession(self.__class__.ALICE_RECIPIENT_ID, 1))

        self.assertTrue(
            bobStore.loadSession(self.__class__.ALICE_RECIPIENT_ID, 1)
            .getSessionState()
            .getSessionVersion()
            == 3
        )
        self.assertTrue(
            bobStore.loadSession(self.__class__.ALICE_RECIPIENT_ID, 1)
            .getSessionState()
            .getAliceBaseKey()
            is not None
        )
        self.assertEqual(originalMessage, plaintext)

        bobOutgoingMessage = bobSessionCipher.encrypt(originalMessage)
        self.assertTrue(bobOutgoingMessage.getType() == CiphertextMessage.WHISPER_TYPE)

        alicePlaintext = aliceSessionCipher.decryptMsg(
            WhisperMessage.from_bytes(bobOutgoingMessage.serialize())
        )
        alicePlaintext = alicePlaintext.decode()
        self.assertEqual(alicePlaintext, originalMessage)

        self.runInteraction(aliceStore, bobStore)

        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(
            aliceStore,
            aliceStore,
            aliceStore,
            aliceStore,
            self.__class__.BOB_RECIPIENT_ID,
            1,
        )
        aliceSessionCipher = SessionCipher(
            aliceStore,
            aliceStore,
            aliceStore,
            aliceStore,
            self.__class__.BOB_RECIPIENT_ID,
            1,
        )

        bobPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeySignature = Curve.calculateSignature(
            bobStore.getIdentityKeyPair().getPrivateKey(),
            bobSignedPreKeyPair.getPublicKey().serialize(),
        )
        bobPreKey = PreKeyBundle(
            bobStore.getLocalRegistrationId(),
            1,
            31338,
            bobPreKeyPair.getPublicKey(),
            23,
            bobSignedPreKeyPair.getPublicKey(),
            bobSignedPreKeySignature,
            bobStore.getIdentityKeyPair().getPublicKey(),
        )

        bobStore.storePreKey(
            31338, PreKeyRecord.new(bobPreKey.getPreKeyId(), bobPreKeyPair)
        )
        bobStore.storeSignedPreKey(
            23,
            SignedPreKeyRecord.new(
                23,
                int(time.time() * 1000),
                bobSignedPreKeyPair,
                bobSignedPreKeySignature,
            ),
        )
        aliceSessionBuilder.processPreKeyBundle(bobPreKey)

        outgoingMessage = aliceSessionCipher.encrypt(originalMessage)

        try:
            plaintext = bobSessionCipher.decryptPkmsg(
                PreKeyWhisperMessage.from_bytes(outgoingMessage)
            )
            raise AssertionError("shouldn't be trusted!")
        except Exception:
            bobStore.saveIdentity(
                self.__class__.ALICE_RECIPIENT_ID,
                PreKeyWhisperMessage.from_bytes(
                    outgoingMessage.serialize()
                ).getIdentityKey(),
            )

        plaintext = bobSessionCipher.decryptPkmsg(
            PreKeyWhisperMessage.from_bytes(outgoingMessage.serialize())
        )
        plaintext = plaintext.decode()
        self.assertEqual(plaintext, originalMessage)

        bobPreKey = PreKeyBundle(
            bobStore.getLocalRegistrationId(),
            1,
            31337,
            Curve.generateKeyPair().getPublicKey(),
            23,
            bobSignedPreKeyPair.getPublicKey(),
            bobSignedPreKeySignature,
            aliceStore.getIdentityKeyPair().getPublicKey(),
        )
        try:
            aliceSessionBuilder.process(bobPreKey)
            raise AssertionError("shouldn't be trusted!")
        except Exception:
            # good
            pass

    def test_badSignedPreKeySignature(self):
        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(
            aliceStore,
            aliceStore,
            aliceStore,
            aliceStore,
            self.__class__.BOB_RECIPIENT_ID,
            1,
        )

        bobIdentityKeyStore = InMemoryIdentityKeyStore()

        bobPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeySignature = Curve.calculateSignature(
            bobIdentityKeyStore.getIdentityKeyPair().getPrivateKey(),
            bobSignedPreKeyPair.getPublicKey().serialize(),
        )

        for i in range(0, len(bobSignedPreKeySignature) * 8):
            modifiedSignature = bytearray(bobSignedPreKeySignature[:])
            modifiedSignature[int(i / 8)] ^= 0x01 << (i % 8)

            bobPreKey = PreKeyBundle(
                bobIdentityKeyStore.getLocalRegistrationId(),
                1,
                31337,
                bobPreKeyPair.getPublicKey(),
                22,
                bobSignedPreKeyPair.getPublicKey(),
                bytes(modifiedSignature),
                bobIdentityKeyStore.getIdentityKeyPair().getPublicKey(),
            )

            with self.assertRaises(InvalidKeyException):
                aliceSessionBuilder.processPreKeyBundle(bobPreKey)

        bobPreKey = PreKeyBundle(
            bobIdentityKeyStore.getLocalRegistrationId(),
            1,
            31337,
            bobPreKeyPair.getPublicKey(),
            22,
            bobSignedPreKeyPair.getPublicKey(),
            bobSignedPreKeySignature,
            bobIdentityKeyStore.getIdentityKeyPair().getPublicKey(),
        )

        aliceSessionBuilder.processPreKeyBundle(bobPreKey)

    def runInteraction(self, aliceStore, bobStore):
        """
        :type aliceStore: AxolotlStore
        :type  bobStore: AxolotlStore
        """
        aliceSessionCipher = SessionCipher(
            aliceStore,
            aliceStore,
            aliceStore,
            aliceStore,
            self.__class__.BOB_RECIPIENT_ID,
            1,
        )
        bobSessionCipher = SessionCipher(
            bobStore, bobStore, bobStore, bobStore, self.__class__.ALICE_RECIPIENT_ID, 1
        )

        originalMessage = "smert ze smert"
        aliceMessage = aliceSessionCipher.encrypt(originalMessage)

        self.assertTrue(aliceMessage.getType() == CiphertextMessage.WHISPER_TYPE)

        plaintext = bobSessionCipher.decryptMsg(
            WhisperMessage.from_bytes(aliceMessage.serialize())
        )
        plaintext = plaintext.decode()
        self.assertEqual(plaintext, originalMessage)

        bobMessage = bobSessionCipher.encrypt(originalMessage)

        self.assertTrue(bobMessage.getType() == CiphertextMessage.WHISPER_TYPE)

        plaintext = aliceSessionCipher.decryptMsg(
            WhisperMessage.from_bytes(bobMessage.serialize())
        )
        plaintext = plaintext.decode()
        self.assertEqual(plaintext, originalMessage)

        for i in range(0, 10):
            loopingMessage = (
                "What do we mean by saying that existence precedes essence? "
                "We mean that man first of all exists, encounters himself, "
                "surges up in the world--and defines himself aftward. %s" % i
            )
            aliceLoopingMessage = aliceSessionCipher.encrypt(loopingMessage)
            loopingPlaintext = bobSessionCipher.decryptMsg(
                WhisperMessage.from_bytes(aliceLoopingMessage.serialize())
            )
            loopingPlaintext = loopingPlaintext.decode()
            self.assertEqual(loopingPlaintext, loopingMessage)

        for i in range(0, 10):
            loopingMessage = (
                "What do we mean by saying that existence precedes essence? "
                "We mean that man first of all exists, encounters himself, "
                "surges up in the world--and defines himself aftward. %s" % i
            )
            bobLoopingMessage = bobSessionCipher.encrypt(loopingMessage)

            loopingPlaintext = aliceSessionCipher.decryptMsg(
                WhisperMessage.from_bytes(bobLoopingMessage.serialize())
            )
            loopingPlaintext = loopingPlaintext.decode()
            self.assertEqual(loopingPlaintext, loopingMessage)

        aliceOutOfOrderMessages = []

        for i in range(0, 10):
            loopingMessage = (
                "What do we mean by saying that existence precedes essence? "
                "We mean that man first of all exists, encounters himself, "
                "surges up in the world--and defines himself aftward. %s" % i
            )
            aliceLoopingMessage = aliceSessionCipher.encrypt(loopingMessage)
            aliceOutOfOrderMessages.append((loopingMessage, aliceLoopingMessage))

        for i in range(0, 10):
            loopingMessage = (
                "What do we mean by saying that existence precedes essence? "
                "We mean that man first of all exists, encounters himself, "
                "surges up in the world--and defines himself aftward. %s" % i
            )
            aliceLoopingMessage = aliceSessionCipher.encrypt(loopingMessage)
            loopingPlaintext = bobSessionCipher.decryptMsg(
                WhisperMessage.from_bytes(aliceLoopingMessage.serialize())
            )
            loopingPlaintext = loopingPlaintext.decode()
            self.assertEqual(loopingPlaintext, loopingMessage)

        for i in range(0, 10):
            loopingMessage = "You can only desire based on what you know: %s" % i
            bobLoopingMessage = bobSessionCipher.encrypt(loopingMessage)

            loopingPlaintext = aliceSessionCipher.decryptMsg(
                WhisperMessage.from_bytes(bobLoopingMessage.serialize())
            )
            loopingPlaintext = loopingPlaintext.decode()
            self.assertEqual(loopingPlaintext, loopingMessage)

        for aliceOutOfOrderMessage in aliceOutOfOrderMessages:
            outOfOrderPlaintext = bobSessionCipher.decryptMsg(
                WhisperMessage.from_bytes(aliceOutOfOrderMessage[1].serialize())
            )
            outOfOrderPlaintext = outOfOrderPlaintext.decode()
            self.assertEqual(outOfOrderPlaintext, aliceOutOfOrderMessage[0])
