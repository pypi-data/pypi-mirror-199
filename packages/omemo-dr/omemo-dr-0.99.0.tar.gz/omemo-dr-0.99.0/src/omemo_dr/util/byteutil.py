from __future__ import annotations

from typing import Any
from typing import Optional


class ByteUtil:
    @staticmethod
    def combine(*args: Any) -> bytearray:
        baos = bytearray()
        for a in args:
            if isinstance(a, (list, bytearray, str, bytes)):
                baos.extend(a)  # pyright: ignore
            else:
                baos.append(a)

        return baos

    @staticmethod
    def split(
        inp: bytes,
        firstLength: int,
        secondLength: int,
        thirdLength: Optional[int] = None,
    ) -> list[bytes]:
        parts: list[bytes] = []
        parts.append(inp[:firstLength])
        parts.append(inp[firstLength : firstLength + secondLength])
        if thirdLength is not None:
            start = firstLength + secondLength
            end = firstLength + secondLength + thirdLength
            parts.append(inp[start:end])

        return parts

    @staticmethod
    def trim(inp: bytes, length: int) -> bytes:
        return inp[:length]

    @staticmethod
    def intsToByteHighAndLow(highValue: int, lowValue: int) -> int:
        return ((highValue << 4 | lowValue) & 0xFF) % 256

    @staticmethod
    def highBitsToInt(value: int) -> int:
        bit = ord(value) if type(value) is str else value
        return (bit & 0xFF) >> 4
