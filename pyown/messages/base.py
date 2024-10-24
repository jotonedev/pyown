from __future__ import annotations

import abc
import copy
import re
from enum import StrEnum
from typing import Final, Pattern, Self, Any

from ..exceptions import InvalidMessage, InvalidTag
from ..tags import Who, Where
from ..tags.base import is_valid_tag

__all__ = [
    "MessageType",
    "BaseMessage",
    "GenericMessage",
    "parse_message",
]


class MessageType(StrEnum):
    ACK = "ACK"
    NACK = "NACK"
    NORMAL = "NORMAL"
    STATUS_REQUEST = "STATUS REQUEST"
    DIMENSION_REQUEST = "DIMENSION REQUEST"
    DIMENSION_WRITING = "DIMENSION WRITING"
    DIMENSION_RESPONSE = "DIMENSION RESPONSE"
    GENERIC = "GENERIC"


class BaseMessage(abc.ABC):
    """
    Base class for all the messages from the OpenWebNet bus.

    It defines the structure of the messages and the methods to parse and create them.

    Attributes:
        prefix (str): Prefix of the message
        suffix (str): Suffix of the message
        separator (str): Separator of the tags
    """
    _type: MessageType = MessageType.GENERIC  # Type of the message
    _tags: Any  # Contains the tags of the message

    prefix: Final[str] = "*"  # Prefix of the message
    suffix: Final[str] = "##"  # Suffix of the message
    separator: Final[str] = "*"  # Separator of the tags

    _regex: Pattern[str] = re.compile(r"^\*(?:([0-9]*)(?:#[0-9]*)*\*?)+##$")  # Regex pattern used to match the message

    @abc.abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {','.join([str(tag) for tag in self._tags])}>"

    def __hash__(self) -> int:
        return hash((self._type, self._tags))

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self._type == other._type and self._tags == other._tags
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    @classmethod
    def pattern(cls) -> Pattern[str]:
        """
        Returns the regex pattern used to match the message represented by the class.
        Returns:
            Pattern[str]: The regex pattern used to match the message
        """
        return cls._regex

    @property
    def tags(self) -> tuple[str] | list[str]:
        """
        Returns a copy of the tags.

        The tags are the elements that compose the message, like the WHO, WHAT, WHERE, etc.

        Returns:
            tuple[str] | list[str]: The tags of the message
        """
        # Returns a new copy of the tags to avoid modifications
        return copy.deepcopy(self._tags)

    @property
    def type(self) -> MessageType:
        """
        Returns the type of the message.

        Returns:
            MessageType: The type of the message
        """
        return self._type

    @property
    @abc.abstractmethod
    def message(self) -> str:
        """
        Returns the message represented by the class.

        This function is equivalent to the `__str__` method.

        Returns:
            str: The message
        """
        raise NotImplementedError

    @property
    def bytes(self) -> bytes:
        """
        Returns the message encoded in bytes.

        Returns:
            bytes: The message encoded in bytes
        """
        return self.message.encode("ascii")

    @classmethod
    @abc.abstractmethod
    def parse(cls, tags: list[str]) -> BaseMessage:
        """
        Parses the tags of a message and returns an instance of the class.
        """
        raise NotImplementedError

    @property
    def who(self) -> Who | None:
        """
        Returns the WHO tag of the message.
        """
        return None

    @property
    def where(self) -> Where | None:
        """
        Returns the WHERE tag of the message.
        """
        return None


class GenericMessage(BaseMessage):
    """
    Represents a generic message.

    This is used when the message has an unknown structure, or to send specific messages that
    don't need a specific class to represent them.
    """

    def __init__(self, tags: list[str]):
        self._tags = tags

    @property
    def message(self) -> str:
        """
        Returns the string representation of the message.

        Returns:
            str: The message
        """
        return f"*{'*'.join(self._tags)}##"

    @classmethod
    def parse(cls, tags: list[str]) -> Self:
        """
        Parses the tags of a message from the OpenWebNet bus.
        In this case, it only checks if the tags are correct.

        Args:
            tags: The tags of the message

        Returns:
            GenericMessage: The instance of the class
        """
        for tag in tags:
            if not is_valid_tag(tag):
                raise InvalidTag(tag)

        return cls(tags=tags)


def parse_message(message: str) -> BaseMessage:
    """
    Parses a message from the OpenWebNet bus.

    Args:
        message (str): The message to parse

    Returns:
        BaseMessage: The appropriate message class instance,
            GenericMessage if the message has an unknown WHO tag or its structure is unknown
    """
    if message.count(BaseMessage.suffix) != 1:
        raise InvalidMessage(message=message)

    message = message.strip()

    tags = message.removeprefix(BaseMessage.prefix).removesuffix(BaseMessage.suffix).split(BaseMessage.separator)

    # First, check if the message is valid
    if GenericMessage.pattern().match(message) is None:
        raise InvalidMessage(message)

    # Then, check if the message is a known message
    # if not, return a GenericMessage
    for subclass in BaseMessage.__subclasses__():
        if subclass is GenericMessage:
            continue

        # noinspection PyUnresolvedReferences
        match = subclass.pattern().match(message)
        if match is not None:
            return subclass.parse(tags)

    # Default case
    return GenericMessage.parse(tags)
