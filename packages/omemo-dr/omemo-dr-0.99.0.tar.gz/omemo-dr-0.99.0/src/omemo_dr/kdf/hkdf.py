from __future__ import annotations

from typing import Optional

import hashlib
import hmac
import math


class HKDF:
    HASH_OUTPUT_SIZE = 32

    def __init__(self, sessionVersion: int) -> None:
        if sessionVersion not in (2, 3, 4):
            raise AssertionError("Unknown version: %s " % sessionVersion)

        self.sessionVersion = sessionVersion

    def deriveSecrets(
        self,
        inputKeyMaterial: bytes,
        info: bytes,
        outputLength: int,
        salt: Optional[bytes] = None,
    ) -> bytes:
        salt = salt or bytearray(self.HASH_OUTPUT_SIZE)
        prk = self.extract(salt, inputKeyMaterial)
        return self.expand(prk, info, outputLength)

    def extract(self, salt: bytes, inputKeyMaterial: bytes) -> bytes:
        mac = hmac.new(bytes(salt), digestmod=hashlib.sha256)
        mac.update(bytes(inputKeyMaterial))
        return mac.digest()

    def expand(self, prk: bytes, info: bytes, outputSize: int) -> bytes:
        iterations = int(math.ceil(float(outputSize) / float(self.HASH_OUTPUT_SIZE)))
        mixin = bytearray()
        results = bytearray()
        remainingBytes = outputSize

        for i in range(
            self.getIterationStartOffset(), iterations + self.getIterationStartOffset()
        ):
            mac = hmac.new(prk, digestmod=hashlib.sha256)
            mac.update(bytes(mixin))
            if info is not None:
                mac.update(bytes(info))
            updateChr = chr(i % 256)
            mac.update(updateChr.encode())

            stepResult = mac.digest()
            stepSize = min(remainingBytes, len(stepResult))
            results.extend(stepResult[:stepSize])
            mixin = stepResult
            remainingBytes -= stepSize

        return bytes(results)

    def getIterationStartOffset(self) -> int:
        if self.sessionVersion == 2:
            return 0
        return 1
