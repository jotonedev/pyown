from enum import IntEnum

from ..messages import GenericMessage

__all__ = [
    "AuthAlgorithm",
]


class AuthAlgorithm(IntEnum):
    SHA1 = 1
    SHA256 = 2

    def to_message(self) -> GenericMessage:
        return GenericMessage(["98", str(self.value)])
