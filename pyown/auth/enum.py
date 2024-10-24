from enum import IntEnum

from ..messages import GenericMessage

__all__ = [
    "AuthAlgorithm",
]


class AuthAlgorithm(IntEnum):
    """
    Represents the all allowed hashing algorithms when using the HMAC authentication algorithm.

    Attributes:
        SHA1: The SHA1 hashing algorithm.
        SHA256: The SHA256 hashing algorithm
    """
    SHA1 = 1
    SHA256 = 2

    def to_message(self) -> GenericMessage:
        """
        Converts the AuthAlgorithm to a message.

        Returns:
            GenericMessage: The message.
        """
        return GenericMessage(["98", str(self.value)])

    @classmethod
    def from_string(cls, value: str) -> "AuthAlgorithm":
        """
        Converts a string to an AuthAlgorithm.

        Args:
            value: The string to convert.

        Returns:
            AuthAlgorithm: The corresponding AuthAlgorithm.
        """
        if value == "1":
            return cls.SHA1
        elif value == "2":
            return cls.SHA256
        else:
            raise ValueError("Invalid hash algorithm")
