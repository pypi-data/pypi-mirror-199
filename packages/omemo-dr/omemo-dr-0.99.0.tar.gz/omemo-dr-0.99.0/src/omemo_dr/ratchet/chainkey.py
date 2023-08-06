from __future__ import annotations

import hashlib
import hmac

from ..kdf.derivedmessagesecrets import DerivedMessageSecrets
from ..kdf.hkdf import HKDF
from ..kdf.messagekeys import MessageKeys


class ChainKey:
    MESSAGE_KEY_SEED = bytearray([0x01])
    CHAIN_KEY_SEED = bytearray([0x02])

    def __init__(self, kdf: HKDF, key: bytes, index: int) -> None:
        self.kdf = kdf
        self.key = key
        self.index = index

    def getKey(self) -> bytes:
        return self.key

    def getIndex(self) -> int:
        return self.index

    def getNextChainKey(self) -> ChainKey:
        nextKey = self.getBaseMaterial(self.__class__.CHAIN_KEY_SEED)
        return ChainKey(self.kdf, nextKey, self.index + 1)

    def getMessageKeys(self) -> MessageKeys:
        if self.kdf.sessionVersion <= 3:
            domain_separator = "WhisperMessageKeys"
        else:
            domain_separator = "OMEMO Message Key Material"

        inputKeyMaterial = self.getBaseMaterial(self.__class__.MESSAGE_KEY_SEED)
        keyMaterialBytes = self.kdf.deriveSecrets(
            inputKeyMaterial,
            bytearray(domain_separator.encode()),
            DerivedMessageSecrets.SIZE,
        )
        keyMaterial = DerivedMessageSecrets(keyMaterialBytes)
        return MessageKeys(
            keyMaterial.getCipherKey(),
            keyMaterial.getMacKey(),
            keyMaterial.getIv(),
            self.index,
        )

    def getBaseMaterial(self, seedBytes: bytes) -> bytes:
        mac = hmac.new(bytes(self.key), digestmod=hashlib.sha256)
        mac.update(bytes(seedBytes))
        return mac.digest()
