from .base import Tag

__all__ = [
    "Dimension",
]


class Dimension(Tag):
    """
    Represent the DIMENSION tag.

    It's not clear in the official documentation what exactly is the DIMENSION tag.
    But in many cases it's used to request information about the status of a device,
    making it similar to the WHAT tag.
    The difference between the two is that the DIMENSION tag does not allow parameters.
    """
    pass
