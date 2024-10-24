import re
from typing import Self, Pattern

from .base import BaseMessage, MessageType
from ..exceptions import InvalidMessage

__all__ = [
    "ACK",
]


class ACK(BaseMessage):
    """
    Represents an ACK message.
    Used to acknowledge a command sent or to end a list of messages sent as a result of a command.

    Syntax: `*#*1##` (constant string)
    """
    _type: MessageType = MessageType.ACK
    _tags: tuple[str, str] = ("#", "1")

    _regex: Pattern[str] = re.compile(r"^\*#\*1##$")

    def __init__(self):
        pass

    @property
    def message(self) -> str:
        """
        Returns the string representation of the message.

        It's a constant string: `*#*1##`
        """
        return "*#*1##"

    @classmethod
    def parse(cls, tags: list[str]) -> Self:
        """
        Parses the tags of a message from the OpenWebNet bus.
        In this case, it only checks if the tags are correct.
        """
        # the first tag bust be #
        if tags[0] != "#" and tags[1] != "1":
            raise InvalidMessage(message="Invalid ACK message")

        return cls()
