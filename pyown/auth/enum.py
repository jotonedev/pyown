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

    @classmethod
    def from_string(cls, value: str) -> "AuthAlgorithm":
        if value == "1":
            return cls.SHA1
        elif value == "2":
            return cls.SHA256
        else:
            raise ValueError("Invalid hash algorithm")
