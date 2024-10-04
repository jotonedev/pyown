from enum import StrEnum, Enum, auto

from ..messages import GenericMessage

__all__ = [
    'SessionType',
    'AuthType',
]


class SessionType(StrEnum):
    # Values documented in the OpenWebNet Intro document
    CommandSession = "9"
    EventSession = "1"
    # Used by the Bticino Virtual Configurator software
    # also called MyHomeSuite
    # This is not documented
    OldCommandSession = "0"

    def to_message(self) -> GenericMessage:
        return GenericMessage.parse(tags=["99", self.value])


class AuthType(Enum):
    Open = auto()
    Hmac = auto()
    NoAuth = auto()
