from ..util.byteutil import ByteUtil


class DerivedMessageSecrets:
    SIZE = 80
    CIPHER_KEY_LENGTH = 32
    MAC_KEY_LENGTH = 32
    IV_LENGTH = 16

    def __init__(self, okm: bytes) -> None:
        keys = ByteUtil.split(
            okm, self.CIPHER_KEY_LENGTH, self.MAC_KEY_LENGTH, self.IV_LENGTH
        )
        self.cipherKey = keys[0]  # AES
        self.macKey = keys[1]  # sha256
        self.iv = keys[2]

    def getCipherKey(self) -> bytes:
        return self.cipherKey

    def getMacKey(self) -> bytes:
        return self.macKey

    def getIv(self) -> bytes:
        return self.iv
