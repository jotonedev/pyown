import re
from typing import Self, Pattern, AnyStr, Final

from .base import BaseMessage, MessageType
from ..tags import Who, Where, Dimension, Value

__all__ = [
    "DimensionRequest",
    "DimensionWriting",
    "DimensionResponse",
]


class DimensionRequest(BaseMessage):
    """
    Represent a dimension request message

    Syntax: *#who*where*dimension##

    This is sent by the client to the server
    """
    _type: Final[MessageType] = MessageType.DIMENSION_REQUEST
    _tags: Final[tuple[Who, Where, Dimension]]

    _regex: Pattern[AnyStr] = re.compile(r"^\*#[0-9#]+\*[0-9#]*\*[0-9]*##$")

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
        """Parse the tags of a message from the OpenWebNet bus."""

        return cls(
            tags=(
                Who(tags[0].removeprefix("#")),
                Where(tags[1]),
                Dimension(tags[2])
            )
        )


class DimensionWriting(BaseMessage):
    """
    Represent a dimension writing message

    Syntax: *#who*where*#dimension*value1*value2*...*valueN##

    This is sent by the client to the server
    """
    _type: MessageType = MessageType.DIMENSION_WRITING
    _tags: Final[tuple[Who, Where, Dimension, Value, ...]]

    _regex: Pattern[AnyStr] = re.compile(r"^\*#[0-9#]+\*[0-9#]*\*#[0-9]*(?:\*[0-9#]*)*##$")

    def __init__(self, tags: tuple[Who, Where, Dimension, Value, ...]):
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
    def values(self) -> tuple[Value]:
        return self._tags[3:]

    @property
    def message(self) -> str:
        return f"*#{self.who}*{self.where}*#{self.dimension}*{'*'.join(self.values)}##"

    @classmethod
    def parse(cls, tags: list[str]) -> Self:
        """Parse the tags of a message from the OpenWebNet bus."""

        values: list[Value] = [Value(t) for t in tags[3:]]

        # noinspection PyTypeChecker
        return cls(
            tags=(
                Who(tags[0].removeprefix("#")),
                Where(tags[1]),
                Dimension(tags[2]).removeprefix("#"),
                *values
            )
        )


class DimensionResponse(DimensionWriting, BaseMessage):
    """
    Represent a dimension writing message

    Syntax: *#who*where*dimension*value1*value2*...*valueN##

    This is sent by the server to the client
    """
    _type: Final[MessageType] = MessageType.DIMENSION_RESPONSE
    _regex: Pattern[AnyStr] = re.compile(r"^\*#[0-9#]+\*[0-9#]*\*[0-9]*(?:\*[0-9#]*)*##$")

    @property
    def message(self) -> str:
        return f"*#{self.who}*{self.where}*{self.dimension}*{'*'.join(self.values)}##"
