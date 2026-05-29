import re
from typing import Pattern, Self

from ..tags import Dimension, Value, Where, Who
from .base import BaseMessage, MessageType

__all__ = [
    "DimensionRequest",
    "DimensionWriting",
    "DimensionResponse",
]


class DimensionRequest(BaseMessage):
    """Represents a dimension request message.

    Syntax: `*#who*where*dimension##`
    """

    _type: MessageType = MessageType.DIMENSION_REQUEST
    _tags: tuple[Who, Where, Dimension]

    _regex: Pattern[str] = re.compile(r"^\*#[0-9#]+\*[0-9]*(?:#[0-9]*)*\*[0-9]*##$")

    def __init__(self, tags: tuple[Who, Where, Dimension]):
        self._tags = tags

    @property
    def who(self) -> Who:
        """The WHO tag of the message."""
        return self._tags[0]

    @property
    def where(self) -> Where:
        """The WHERE tag of the message."""
        return self._tags[1]

    @property
    def dimension(self) -> Dimension:
        """The DIMENSION tag of the message."""
        return self._tags[2]

    @property
    def message(self) -> str:
        """The string representation of the message as sent on the bus."""
        return f"*#{self.who}*{self.where}*{self.dimension}##"

    @classmethod
    def parse(cls, tags: list[str]) -> Self:
        """Parses the tags of a message from the OpenWebNet bus."""
        return cls(tags=(Who(tags[0].removeprefix("#")), Where(tags[1]), Dimension(tags[2])))


class DimensionWriting(BaseMessage):
    """Represents a dimension writing message.

    Syntax: `*#who*where*#dimension*value1*value2*...*valueN##`
    """

    _type: MessageType = MessageType.DIMENSION_WRITING
    _tags: tuple[Who, Where, Dimension, *tuple[Value, ...]]

    _regex: Pattern[str] = re.compile(
        r"^\*#[0-9#]+\*[0-9]*(?:#[0-9]*)*\*#[0-9]*(?:\*[0-9]*(?:#[0-9]*)*)*##$"
    )

    def __init__(self, tags: tuple[Who, Where, Dimension, *tuple[Value, ...]]):
        self._tags = tags

    @property
    def who(self) -> Who:
        """The WHO tag of the message."""
        return self._tags[0]

    @property
    def where(self) -> Where:
        """The WHERE tag of the message."""
        return self._tags[1]

    @property
    def dimension(self) -> Dimension:
        """The DIMENSION tag of the message."""
        return self._tags[2]

    @property
    def values(self) -> tuple[Value, ...]:
        """The VALUE tags of the message."""
        return self._tags[3:]

    @property
    def message(self) -> str:
        """The string representation of the message as sent on the bus."""
        return f"*#{self.who}*{self.where}*#{self.dimension}*{'*'.join([str(value) for value in self.values])}##"

    @classmethod
    def parse(cls, tags: list[str]) -> Self:
        """Parses the tags of a message from the OpenWebNet bus."""
        values: list[Value] = [Value(t) for t in tags[3:]]

        # noinspection PyTypeChecker
        return cls(
            tags=(
                Who(tags[0].removeprefix("#")),
                Where(tags[1]),
                Dimension(tags[2].removeprefix("#")),
                *values,
            )
        )


class DimensionResponse(DimensionWriting, BaseMessage):
    """Represents a dimension writing message.

    Syntax: `*#who*where*dimension*value1*value2*...*valueN##`
    """

    _type: MessageType = MessageType.DIMENSION_RESPONSE
    _regex: Pattern[str] = re.compile(
        r"^\*#[0-9#]+\*[0-9]*(?:#[0-9]*)*\*[0-9]*(?:#[0-9]*)*(?:\*[0-9]*(?:#[0-9]*)*)*##$"
    )

    @property
    def message(self) -> str:
        """The string representation of the message as sent on the bus."""
        return f"*#{self.who}*{self.where}*{self.dimension}*{'*'.join([str(value) for value in self.values])}##"
