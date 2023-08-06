import unittest

from omemo_dr.kdf.hkdf import HKDF
from omemo_dr.ratchet.chainkey import ChainKey


class ChainKeyTest(unittest.TestCase):
    def test_chainKeyDerivationV2(self):
        seed = bytearray(
            [
                0x8A,
                0xB7,
                0x2D,
                0x6F,
                0x4C,
                0xC5,
                0xAC,
                0x0D,
                0x38,
                0x7E,
                0xAF,
                0x46,
                0x33,
                0x78,
                0xDD,
                0xB2,
                0x8E,
                0xDD,
                0x07,
                0x38,
                0x5B,
                0x1C,
                0xB0,
                0x12,
                0x50,
                0xC7,
                0x15,
                0x98,
                0x2E,
                0x7A,
                0xD4,
                0x8F,
            ]
        )

        messageKey = bytearray(
            [
                0x02,
                0xA9,
                0xAA,
                0x6C,
                0x7D,
                0xBD,
                0x64,
                0xF9,
                0xD3,
                0xAA,
                0x92,
                0xF9,
                0x2A,
                0x27,
                0x7B,
                0xF5,
                0x46,
                0x09,
                0xDA,
                0xDF,
                0x0B,
                0x00,
                0x82,
                0x8A,
                0xCF,
                0xC6,
                0x1E,
                0x3C,
                0x72,
                0x4B,
                0x84,
                0xA7,
            ]
        )

        macKey = bytearray(
            [
                0xBF,
                0xBE,
                0x5E,
                0xFB,
                0x60,
                0x30,
                0x30,
                0x52,
                0x67,
                0x42,
                0xE3,
                0xEE,
                0x89,
                0xC7,
                0x02,
                0x4E,
                0x88,
                0x4E,
                0x44,
                0x0F,
                0x1F,
                0xF3,
                0x76,
                0xBB,
                0x23,
                0x17,
                0xB2,
                0xD6,
                0x4D,
                0xEB,
                0x7C,
                0x83,
            ]
        )

        nextChainKey = bytearray(
            [
                0x28,
                0xE8,
                0xF8,
                0xFE,
                0xE5,
                0x4B,
                0x80,
                0x1E,
                0xEF,
                0x7C,
                0x5C,
                0xFB,
                0x2F,
                0x17,
                0xF3,
                0x2C,
                0x7B,
                0x33,
                0x44,
                0x85,
                0xBB,
                0xB7,
                0x0F,
                0xAC,
                0x6E,
                0xC1,
                0x03,
                0x42,
                0xA2,
                0x46,
                0xD1,
                0x5D,
            ]
        )

        chainKey = ChainKey(HKDF(2), seed, 0)
        self.assertEqual(chainKey.getKey(), seed)
        self.assertEqual(chainKey.getMessageKeys().getCipherKey(), messageKey)
        self.assertEqual(chainKey.getMessageKeys().getMacKey(), macKey)
        self.assertEqual(chainKey.getNextChainKey().getKey(), nextChainKey)
        self.assertEqual(chainKey.getIndex(), 0)
        self.assertEqual(chainKey.getMessageKeys().getCounter(), 0)
        self.assertEqual(chainKey.getNextChainKey().getIndex(), 1)
        self.assertEqual(chainKey.getNextChainKey().getMessageKeys().getCounter(), 1)
