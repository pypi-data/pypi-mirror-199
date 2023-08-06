import unittest

from omemo_dr.ecc.curve import Curve
from omemo_dr.ecc.eckeypair import ECKeyPair
from omemo_dr.identitykey import IdentityKey
from omemo_dr.identitykeypair import IdentityKeyPair
from omemo_dr.ratchet.bobaxolotlparamaters import BobAxolotlParameters
from omemo_dr.ratchet.ratchetingsession import RatchetingSession
from omemo_dr.state.sessionstate import SessionState


class RatchetingSessionTest(unittest.TestCase):
    def test_ratchetingSessionAsBob(self):
        bobPublic = bytearray(
            [
                0x05,
                0x2C,
                0xB4,
                0x97,
                0x76,
                0xB8,
                0x77,
                0x02,
                0x05,
                0x74,
                0x5A,
                0x3A,
                0x6E,
                0x24,
                0xF5,
                0x79,
                0xCD,
                0xB4,
                0xBA,
                0x7A,
                0x89,
                0x04,
                0x10,
                0x05,
                0x92,
                0x8E,
                0xBB,
                0xAD,
                0xC9,
                0xC0,
                0x5A,
                0xD4,
                0x58,
            ]
        )

        bobPrivate = bytearray(
            [
                0xA1,
                0xCA,
                0xB4,
                0x8F,
                0x7C,
                0x89,
                0x3F,
                0xAF,
                0xA9,
                0x88,
                0x0A,
                0x28,
                0xC3,
                0xB4,
                0x99,
                0x9D,
                0x28,
                0xD6,
                0x32,
                0x95,
                0x62,
                0xD2,
                0x7A,
                0x4E,
                0xA4,
                0xE2,
                0x2E,
                0x9F,
                0xF1,
                0xBD,
                0xD6,
                0x5A,
            ]
        )

        bobIdentityPublic = bytearray(
            [
                0x05,
                0xF1,
                0xF4,
                0x38,
                0x74,
                0xF6,
                0x96,
                0x69,
                0x56,
                0xC2,
                0xDD,
                0x47,
                0x3F,
                0x8F,
                0xA1,
                0x5A,
                0xDE,
                0xB7,
                0x1D,
                0x1C,
                0xB9,
                0x91,
                0xB2,
                0x34,
                0x16,
                0x92,
                0x32,
                0x4C,
                0xEF,
                0xB1,
                0xC5,
                0xE6,
                0x26,
            ]
        )

        bobIdentityPrivate = bytearray(
            [
                0x48,
                0x75,
                0xCC,
                0x69,
                0xDD,
                0xF8,
                0xEA,
                0x07,
                0x19,
                0xEC,
                0x94,
                0x7D,
                0x61,
                0x08,
                0x11,
                0x35,
                0x86,
                0x8D,
                0x5F,
                0xD8,
                0x01,
                0xF0,
                0x2C,
                0x02,
                0x25,
                0xE5,
                0x16,
                0xDF,
                0x21,
                0x56,
                0x60,
                0x5E,
            ]
        )

        aliceBasePublic = bytearray(
            [
                0x05,
                0x47,
                0x2D,
                0x1F,
                0xB1,
                0xA9,
                0x86,
                0x2C,
                0x3A,
                0xF6,
                0xBE,
                0xAC,
                0xA8,
                0x92,
                0x02,
                0x77,
                0xE2,
                0xB2,
                0x6F,
                0x4A,
                0x79,
                0x21,
                0x3E,
                0xC7,
                0xC9,
                0x06,
                0xAE,
                0xB3,
                0x5E,
                0x03,
                0xCF,
                0x89,
                0x50,
            ]
        )

        # aliceEphemeralPublic = bytearray([0x05, 0x6c, 0x3e, 0x0d, 0x1f, 0x52, 0x02, 0x83, 0xef, 0xcc, 0x55, 0xfc,
        #                                   0xa5, 0xe6, 0x70, 0x75, 0xb9, 0x04, 0x00, 0x7f, 0x18, 0x81, 0xd1, 0x51,
        #                                   0xaf, 0x76, 0xdf, 0x18, 0xc5, 0x1d, 0x29, 0xd3, 0x4b])

        aliceIdentityPublic = bytearray(
            [
                0x05,
                0xB4,
                0xA8,
                0x45,
                0x56,
                0x60,
                0xAD,
                0xA6,
                0x5B,
                0x40,
                0x10,
                0x07,
                0xF6,
                0x15,
                0xE6,
                0x54,
                0x04,
                0x17,
                0x46,
                0x43,
                0x2E,
                0x33,
                0x39,
                0xC6,
                0x87,
                0x51,
                0x49,
                0xBC,
                0xEE,
                0xFC,
                0xB4,
                0x2B,
                0x4A,
            ]
        )

        senderChain = bytearray(
            [
                0xD2,
                0x2F,
                0xD5,
                0x6D,
                0x3F,
                0xEC,
                0x81,
                0x9C,
                0xF4,
                0xC3,
                0xD5,
                0x0C,
                0x56,
                0xED,
                0xFB,
                0x1C,
                0x28,
                0x0A,
                0x1B,
                0x31,
                0x96,
                0x45,
                0x37,
                0xF1,
                0xD1,
                0x61,
                0xE1,
                0xC9,
                0x31,
                0x48,
                0xE3,
                0x6B,
            ]
        )

        bobIdentityKeyPublic = IdentityKey(bobIdentityPublic, 0)
        bobIdentityKeyPrivate = Curve.decodePrivatePoint(bobIdentityPrivate)
        bobIdentityKey = IdentityKeyPair.new(
            bobIdentityKeyPublic, bobIdentityKeyPrivate
        )
        bobEphemeralPublicKey = Curve.decodePoint(bobPublic, 0)
        bobEphemeralPrivateKey = Curve.decodePrivatePoint(bobPrivate)
        bobEphemeralKey = ECKeyPair(bobEphemeralPublicKey, bobEphemeralPrivateKey)
        bobBaseKey = bobEphemeralKey

        aliceBasePublicKey = Curve.decodePoint(aliceBasePublic, 0)
        # aliceEphemeralPublicKey = Curve.decodePoint(aliceEphemeralPublic, 0)
        aliceIdentityPublicKey = IdentityKey(aliceIdentityPublic, 0)

        parameters = (
            BobAxolotlParameters.newBuilder()
            .setOurIdentityKey(bobIdentityKey)
            .setOurSignedPreKey(bobBaseKey)
            .setOurRatchetKey(bobEphemeralKey)
            .setOurOneTimePreKey(None)
            .setTheirIdentityKey(aliceIdentityPublicKey)
            .setTheirBaseKey(aliceBasePublicKey)
            .create()
        )

        session = SessionState()

        RatchetingSession.initializeSessionAsBob(session, 2, parameters)
        self.assertEqual(session.getLocalIdentityKey(), bobIdentityKey.getPublicKey())
        self.assertEqual(session.getRemoteIdentityKey(), aliceIdentityPublicKey)
        self.assertEqual(session.getSenderChainKey().getKey(), senderChain)
