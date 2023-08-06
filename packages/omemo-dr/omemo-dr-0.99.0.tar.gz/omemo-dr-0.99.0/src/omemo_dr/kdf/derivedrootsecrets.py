from ..util.byteutil import ByteUtil


class DerivedRootSecrets:
    SIZE = 64

    def __init__(self, okm: bytes) -> None:
        keys = ByteUtil.split(okm, 32, 32)
        self.rootKey = keys[0]
        self.chainKey = keys[1]

    def getRootKey(self) -> bytes:
        return self.rootKey

    def getChainKey(self) -> bytes:
        return self.chainKey
