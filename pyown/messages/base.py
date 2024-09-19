import abc
import re
import copy

from enum import StrEnum
from typing import Final, TypeVar, Type, Pattern, AnyStr

from ..exceptions import ParseError, InvalidMessage

__all__ = [
    "MessageType",
    "BaseMessage",
    "parse_message",
]


Self = TypeVar("Self", bound="BaseMessage")


class MessageType(StrEnum):
    ACK = "ACK"
    NACK = "NACK"
    NORMAL = "NORMAL"
    STATUS_REQUEST = "STATUS REQUEST"
    STATUS_RESPONSE = "STATUS RESPONSE"
    DIMENSION_REQUEST = "DIMENSION REQUEST"
    DIMENSION_RESPONSE = "DIMENSION RESPONSE"
    GENERIC = "GENERIC"





class BaseMessage(abc.ABC):
    _type: MessageType = MessageType.GENERIC  # Type of the message
    _tags: list[StrEnum, str]  # Contains the tags of the message

    prefix: Final[str] = "*"  # Prefix of the message
    suffix: Final[str] = "##"  # Suffix of the message
    separator: Final[str] = "*"  # Separator of the tags

    _regex: Pattern[AnyStr] = re.compile(r"^\*(?:([0-9#]*)\*)+([0-9#]*)##$")  # Regex pattern used to match the message

    @abc.abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        """
        Return the message as a string.
        Returns:
            str: The message
        """
        return self.message

    def __repr__(self) -> str:
        """
        Return the representation of the message.
        Returns:
            str: The representation
        """
        return f"<{self.__class__.__name__}: {','.join(self.tags)}>"

    def __hash__(self) -> int:
        return hash((self._type, self._tags))

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self._type == other._type and self._tags == other._tags
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    @classmethod
    def pattern(cls) -> Pattern[AnyStr]:
        """
        Return the regex pattern used to match the message represented by the class.
        Returns:
            Pattern[AnyStr]: The regex pattern
        """
        return cls._regex

    @property
    def tags(self) -> list[StrEnum, str]:
        """
        Return the tags of the message.
        The tags are the elements that compose the message, like the WHO, WHAT, WHERE, etc.

        Returns:
            list[StrEnum, str]: The tags of the message
        """
        # Return a new copy of the tags to avoid modifications
        return copy.deepcopy(self._tags)

    @property
    def type(self) -> MessageType:
        """
        Return the type of the message.
        Returns:
            MessageType: The type of the message
        """
        return self._type

    @property
    @abc.abstractmethod
    def message(self) -> str:
        """
        Return the message represented by the class.
        Returns:
            str: The message
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def parse(cls, tags: list[str]) -> Type[Self]:
        """Parse the tags of a message from the OpenWebNet bus."""
        raise NotImplementedError


def parse_message(message: str) -> Type[BaseMessage]:
    """
    Parse a message from the OpenWebNet bus.

    Args:
        message (str): The message to parse

    Returns:
        Type[BaseMessage]: The appropriate message class instance
    """
    if message.count(BaseMessage.suffix) != 1:
        raise InvalidMessage(message=message)

    tags = message.strip().removeprefix(BaseMessage.prefix).removesuffix(BaseMessage.suffix).split(BaseMessage.separator)

    for subclass in BaseMessage.__subclasses__():
        # noinspection PyUnresolvedReferences
        match = subclass.pattern().match(message)
        if match is not None:
            return subclass.parse(tags)
    else:
        raise ParseError(message=message, tags=tags)

