from .base import TagWithParameters

__all__ = [
    "Dimension",
]


class Dimension(TagWithParameters):
    """
    Represents the DIMENSION tag.

    It's used in dimension messages.

    It's not clear in the official documentation what exactly is the DIMENSION tag.
    But in many cases it's used to request information about the status of a device,
    making it similar to the WHAT tag.
    """
    pass
