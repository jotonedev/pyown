from enum import StrEnum

from ..messages import GenericMessage

__all__ = [
    'SessionType',
]


class SessionType(StrEnum):
    """
    Represents the all allowed values for session types in the OpenWebNet protocol.

    Attributes:
        OldCommandSession: Legacy command session value not present in the official OpenWebNet documentation.
        CommandSession: Official command session value. Used to create a session for sending commands.
        EventSession: Event session value. Used to create a session for receiving events,
            sending commands is not allowed.
    """
    OldCommandSession = "0"
    CommandSession = "9"
    EventSession = "1"

    def to_message(self) -> GenericMessage:
        """
        Convert the session type to the session message to send to the gateway.

        Returns:
            GenericMessage: The message to send to the gateway.
        """
        return GenericMessage.parse(tags=["99", self.value])
