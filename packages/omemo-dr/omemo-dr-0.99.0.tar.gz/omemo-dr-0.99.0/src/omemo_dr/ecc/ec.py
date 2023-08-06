import abc


class ECPublicKey(abc.ABC):
    @abc.abstractmethod
    def serialize(self) -> bytes:
        pass

    @abc.abstractmethod
    def getType(self) -> int:
        pass


class ECPrivateKey(abc.ABC):
    @abc.abstractmethod
    def serialize(self) -> bytes:
        pass

    @abc.abstractmethod
    def getType(self) -> int:
        pass
