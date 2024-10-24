import re
from typing import Self, Pattern

from .base import BaseMessage, MessageType
from ..exceptions import InvalidMessage

__all__ = [
    "NACK",
]


class NACK(BaseMessage):
    """
    Represents a NACK message.
    Used to signal that a command sent wasn’t executed correctly, or it's not supported.

    Syntax: `*#*0##` (constant string)
    """
    _type: MessageType = MessageType.NACK
    _tags: tuple[str, str] = ("#", "0")

    _regex: Pattern[str] = re.compile(r"^\*#\*0##$")

    def __init__(self):
        pass

    @property
    def message(self) -> str:
        """
        Returns the string representation of the message.

        It's a constant string: `*#*0##`
        """
        return "*#*0##"

    @classmethod
    def parse(cls, tags: list[str]) -> Self:
        """
        Parses the tags of a message from the OpenWebNet bus.
        In this case, it only checks if the tags are correct.
        """
        # the first tag bust be #
        if tags[0] != "#" and tags[1] != "0":
            raise InvalidMessage(tags)

        return cls()
