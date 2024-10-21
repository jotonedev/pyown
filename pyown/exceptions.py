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
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class ParseError(OWNException):
    tags: list[str]
    message: str

    def __init__(self, tags: list[str], message: str) -> None:
        self.tags = tags
        self.message = message
        super().__init__(f"Error parsing message: {message}")


class InvalidData(OWNException):
    data: bytes

    def __init__(self, data: bytes):
        self.data = data

        super().__init__(f"Error parsing data: {data.hex()}")


class InvalidMessage(OWNException):
    message: str

    def __init__(self, message: Any) -> None:
        self.message = message
        super().__init__(f"Invalid message: {message}")


class InvalidTag(OWNException):
    tag: str

    def __init__(self, tag: Any) -> None:
        self.tag = tag
        super().__init__(f"Invalid tag: {tag}")


class InvalidSession(OWNException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidAuthentication(InvalidSession):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ResponseError(OWNException):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)
