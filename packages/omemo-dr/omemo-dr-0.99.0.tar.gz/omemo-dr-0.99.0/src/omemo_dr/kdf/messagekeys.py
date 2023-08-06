class MessageKeys:
    def __init__(
        self, cipherKey: bytes, macKey: bytes, iv: bytes, counter: int
    ) -> None:
        self.cipherKey = cipherKey
        self.macKey = macKey
        self.iv = iv
        self.counter = counter

    def getCipherKey(self) -> bytes:
        return self.cipherKey

    def getMacKey(self) -> bytes:
        return self.macKey

    def getIv(self) -> bytes:
        return self.iv

    def getCounter(self) -> int:
        return self.counter
