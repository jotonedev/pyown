from abc import ABC
from typing import AsyncIterator, ClassVar

from ..client import BaseClient
from ..exceptions import InvalidMessage, ResponseError
from ..messages import (
    BaseMessage,
    DimensionRequest,
    DimensionResponse,
    DimensionWriting,
    MessageType,
    NormalMessage,
    StatusRequest,
)
from ..tags import Dimension, Value, What, Where, Who

__all__ = ["BaseItem", "EventMessage"]


EventMessage = DimensionResponse | DimensionWriting | None
"""Type alias for the optional message argument accepted by an item's internal
decode helpers, so the same helper can decode an event message or fetch fresh
data from the gateway.
"""


class BaseItem(ABC):
    """The base class for all items.

    Provides the basic functionality to communicate with the gateway. The WHO
    tag is set by the `@item(Who.X)` decorator at class-definition time.
    """

    _who: ClassVar[Who]

    def __init__(self, client: BaseClient, where: Where | str, *, who: Who | str | None = None):
        """Initializes the item.

        Args:
            client: The client to use to communicate with the server.
            where: The location of the item.
            who: The type of item.
        """
        self._client = client

        if isinstance(where, str):
            where = Where(where)
        self._where = where

        if who is not None:
            if isinstance(who, str):
                who = Who(who)
            self._who = who

    def __repr__(self):
        return f"{self.__class__.__name__}(where={self._where})"

    def __str__(self):
        return f"{self.__class__.__name__} at {self._where}"

    @property
    def where(self) -> Where:
        """Returns the where value of the item."""
        return self._where

    @classmethod
    @property
    def who(cls) -> Who:
        """Returns the who value of the item."""
        return cls._who

    @property
    def client(self) -> BaseClient:
        """Returns the client used to communicate with the server."""
        return self._client

    @client.setter
    def client(self, client: BaseClient):
        self._client = client

    async def _send_message(self, message: BaseMessage) -> None:
        """Sends a message to the server.

        Args:
            message: The message to send.

        Returns:
            None
        """
        return await self._client.send_message(message)

    async def _read_message(self, timeout: int | None = 5) -> BaseMessage:
        """Reads a message from the server.

        Args:
            timeout: The time to wait for a message, None to wait indefinitely.

        Returns:
            The message received.
        """
        return await self._client.read_message(timeout=timeout)

    @staticmethod
    def _check_ack(resp: BaseMessage) -> None:
        """Checks if the response is an ACK message.

        Args:
            resp: The response to check.

        Raises:
            ResponseError: If the response is not an ACK message.
        """
        if resp.type != MessageType.ACK:
            raise ResponseError(f"Received {resp} instead of ACK")

    @staticmethod
    def _check_nack(resp: BaseMessage) -> None:
        """Checks if the response is a NACK message.

        Args:
            resp: The response to check.

        Raises:
            ResponseError: If the response is a NACK message.
        """
        if resp.type == MessageType.NACK:
            raise ResponseError(f"Received {resp} instead of NACK")

    def create_normal_message(self, what: What | str) -> NormalMessage:
        """Creates a normal message for the item.

        Args:
            what: The action to perform.

        Returns:
            A normal message.
        """
        if isinstance(what, str):
            what = What(what)

        return NormalMessage((self._who, what, self._where))

    def create_status_message(self) -> StatusRequest:
        """Creates a status message for the item.

        Returns:
            A status message.
        """
        return StatusRequest((self._who, self._where))

    def create_dimension_writing_message(
        self, dimension: Dimension, *args: Value
    ) -> DimensionWriting:
        """Creates a dimension message for the item.

        Args:
            dimension: the dimension value to set.
            *args: the values to set.
        """
        # noinspection PyTypeChecker
        return DimensionWriting(
            (
                self._who,
                self._where,
                dimension,
                *args,
            )
        )

    def create_dimension_request_message(self, dimension: Dimension) -> DimensionRequest:
        """Creates a dimension request message for the item.

        Args:
            dimension: the dimension value to request.
        """
        return DimensionRequest((self._who, self._where, dimension))

    async def send_normal_message(self, what: What | str) -> None:
        """Sends a normal message to the server and check the response.

        Args:
            what: The action to perform.

        Raises:
            ResponseError: If the server does not acknowledge the message.
        """
        msg = self.create_normal_message(what)
        await self._send_message(msg)

        resp = await self._read_message()
        self._check_ack(resp)

    async def send_status_request(self) -> AsyncIterator[NormalMessage]:
        """Sends a status request and receive multiple responses from the server.

        Raises:
            ResponseError: If the server responds with an invalid message.

        Returns:
            The responses from the server.
        """
        msg = self.create_status_message()
        await self._send_message(msg)

        while True:
            resp = await self._read_message()
            self._check_nack(resp)

            # when the server responds with an ACK message, it means that the server has finished sending the responses
            if resp.type == MessageType.ACK:
                break

            if not isinstance(resp, NormalMessage):
                raise ResponseError(f"Received {resp} instead of a normal message")

            yield resp

    async def send_dimension_request(
        self, dimension: Dimension | str
    ) -> AsyncIterator[DimensionResponse]:
        """Sends a dimension request and receive multiple responses from the server.

        Raises:
            ResponseError: If the server responds with an invalid message.

        Returns:
            The responses from the server.
        """
        if isinstance(dimension, str):
            dimension = Dimension(dimension)

        msg = self.create_dimension_request_message(dimension)
        await self._send_message(msg)

        while True:
            resp = await self._read_message()
            self._check_nack(resp)

            # when the server responds with an ACK message, it means that the server has finished sending the responses
            if resp.type == MessageType.ACK:
                break

            if not isinstance(resp, DimensionResponse):
                raise ResponseError(f"Received {resp} instead of a dimension response message")

            yield resp

    async def send_dimension_writing(self, dimension: Dimension | str, *args: Value) -> None:
        """Sends a dimension writing message to the server and check the response.

        Args:
            dimension: the dimension value to set.
            *args: the values to set.

        Raises:
            ResponseError: If the server does not acknowledge the message.
        """
        if isinstance(dimension, str):
            dimension = Dimension(dimension)

        msg = self.create_dimension_writing_message(dimension, *args)
        await self._send_message(msg)

        resp = await self._read_message()
        self._check_ack(resp)

    # TODO: Refactor this method
    async def _single_dim_req(self, what: What | Dimension) -> DimensionResponse:
        """Makes a dimension request and returns only the first response while consuming the rest."""
        if isinstance(what, What):
            what = Dimension(what.string)

        messages = [msg async for msg in self.send_dimension_request(what)]

        if len(messages) == 0:
            raise ResponseError("The server did not respond with data.")

        resp = messages[0]
        if not isinstance(resp, DimensionResponse):
            raise InvalidMessage("The message is not a DimensionResponse message.")
        else:
            return resp
