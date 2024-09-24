class ParseError(Exception):
    tags: list[str]
    message: str

    def __init__(self, tags: list[str], message: str) -> None:
        self.tags = tags
        self.message = message
        super().__init__(f"Error parsing message: {message}")


class InvalidMessage(Exception):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(f"Invalid message: {message}")


class InvalidTag(Exception):
    tag: str

    def __init__(self, tag: str) -> None:
        self.tag = tag
        super().__init__(f"Invalid tag: {tag}")
