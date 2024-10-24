__all__ = [
    "OWNException",
    "ParseError",
    "InvalidData",
    "InvalidMessage",
    "InvalidTag",
    "InvalidSession",
    "InvalidAuthentication",
    "ResponseError",
]

from typing import Any


class OWNException(Exception):
    """
    Base exception for all exceptions in the pyown package.

    This exception should not be raised directly.
    It is useful for catching all exceptions in the package.
    """
    pass


class ParseError(OWNException):
    """
    Raised when an error occurs while parsing a message or a tag.

    It is a generic exception and should not be raised directly.
    """
    pass


class InvalidData(ParseError):
    """
    Raised when an error occurs when not valid data or characters not allowed are received.
    This should not happen with official gateways.

    Args:
        data: The data that caused the error.
    """
    data: bytes

    def __init__(self, data: bytes):
        self.data = data

        super().__init__(f"Error parsing data: {data.hex()}")


class InvalidMessage(ParseError):
    """
    Raised when a message does not follow the protocol standards.

    Args:
        message: The message or tags that caused the error.
    """
    message: str

    def __init__(self, message: str | list[str]) -> None:
        if isinstance(message, list):
            self.message = "*" + "*".join(message) + "##"
        else:
            self.message = message

        super().__init__(f"Invalid message: {self.message}")


class InvalidTag(ParseError):
    """
    Raised when a tag is not valid or does not follow the protocol standards.

    Args:
        tag: The tag that caused the error.
    """
    tag: str

    def __init__(self, tag: Any) -> None:
        self.tag = tag
        super().__init__(f"Invalid tag: {tag}")


class InvalidSession(OWNException):
    """
    Raised when a command is sent using an event session or when event methods are called using a command session.
    """
    pass


class InvalidAuthentication(OWNException):
    """
    Raised when the authentication fails or an unsupported authentication method is used.
    """
    pass


class ResponseError(OWNException):
    """
    Raised when an error the server responds with a NACK or responds with an unexpected message.
    """
    pass
