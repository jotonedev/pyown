import re
from typing import Self, Pattern

from .base import BaseMessage, MessageType
from ..tags import Who, Where, Dimension, Value

__all__ = [
    "DimensionRequest",
    "DimensionWriting",
    "DimensionResponse",
]


class DimensionRequest(BaseMessage):
    """
    Represents a dimension request message

    Syntax: `*#who*where*dimension##`
    """
    _type: MessageType = MessageType.DIMENSION_REQUEST
    _tags: tuple[Who, Where, Dimension]

    _regex: Pattern[str] = re.compile(r"^\*#[0-9#]+\*[0-9]*(?:#[0-9]*)*\*[0-9]*##$")

    def __init__(self, tags: tuple[Who, Where, Dimension]):
        self._tags = tags

    @property
    def who(self) -> Who:
        return self._tags[0]

    @property
    def where(self) -> Where:
        return self._tags[1]

    @property
    def dimension(self) -> Dimension:
        return self._tags[2]

    @property
    def message(self) -> str:
        return f"*#{self.who}*{self.where}*{self.dimension}##"

    @classmethod
    def parse(cls, tags: list[str]) -> Self:
        """Parses the tags of a message from the OpenWebNet bus."""

        return cls(
            tags=(
                Who(tags[0].removeprefix("#")),
                Where(tags[1]),
                Dimension(tags[2])
            )
        )


class DimensionWriting(BaseMessage):
    """
    Represents a dimension writing message

    Syntax: `*#who*where*#dimension*value1*value2*...*valueN##`
    """
    _type: MessageType = MessageType.DIMENSION_WRITING
    _tags: tuple[Who, Where, Dimension, Value, ...]  # type: ignore[misc]

    _regex: Pattern[str] = re.compile(r"^\*#[0-9#]+\*[0-9]*(?:#[0-9]*)*\*#[0-9]*(?:\*[0-9]*(?:#[0-9]*)*)*##$")

    def __init__(self, tags: tuple[Who, Where, Dimension, Value, ...]):  # type: ignore[misc]
        self._tags = tags

    @property
    def who(self) -> Who:
        return self._tags[0]

    @property
    def where(self) -> Where:
        return self._tags[1]

    @property
    def dimension(self) -> Dimension:
        return self._tags[2]

    @property
    def values(self) -> tuple[Value, ...]:
        return self._tags[3:]

    @property
    def message(self) -> str:
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
                *values  # type: ignore[arg-type]
            )
        )


class DimensionResponse(DimensionWriting, BaseMessage):
    """
    Represents a dimension writing message

    Syntax: `*#who*where*dimension*value1*value2*...*valueN##`
    """
    _type: MessageType = MessageType.DIMENSION_RESPONSE
    _regex: Pattern[str] = re.compile(
        r"^\*#[0-9#]+\*[0-9]*(?:#[0-9]*)*\*[0-9]*(?:#[0-9]*)*(?:\*[0-9]*(?:#[0-9]*)*)*##$")

    @property
    def message(self) -> str:
        return f"*#{self.who}*{self.where}*{self.dimension}*{'*'.join([str(value) for value in self.values])}##"
