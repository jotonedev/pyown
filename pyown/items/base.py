from abc import ABC

from ..client import BaseClient
from ..exceptions import RequestError
from ..messages import NormalMessage, StatusRequest, DimensionWriting, DimensionRequest, BaseMessage, MessageType
from ..tags import Where, Who, What, Dimension, Value

__all__ = [
    "BaseEvents",
    "BaseItem",
]


class BaseEvents:
    pass


class BaseItem(ABC):
    _who = Who.LIGHTING

    def __init__(self, client: BaseClient, where: Where | str, *, who: Who | str | None = None):
        """
        Initialize the item.
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
    def where(self):
        return self._where

    @property
    def who(self):
        return self._who

    async def _send_message(self, message: BaseMessage) -> None:
        """
        Send a message to the server
        Args:
            message: The message to send.

        Returns:
            None
        """
        return await self._client.send_message(message)

    async def _read_message(self, timeout: int | None = 5) -> BaseMessage:
        """
        Read a message from the server
        Args:
            timeout: The time to wait for a message, None to wait indefinitely.

        Returns:
            The message received.
        """
        return await self._client.read_message(timeout=timeout)

    @staticmethod
    def _check_ack(resp: BaseMessage) -> None:
        """
        Check if the response is an ACK message.
        Args:
            resp: The response to check.

        Raises:
            RequestError: If the response is not an ACK message.
        """
        if resp.type != MessageType.ACK:
            raise RequestError(f"Received {resp} instead of ACK")

    @staticmethod
    def _check_nack(resp: BaseMessage) -> None:
        """
        Check if the response is a NACK message.
        Args:
            resp: The response to check.

        Raises:
            RequestError: If the response is a NACK message.
        """
        if resp.type == MessageType.NACK:
            raise RequestError(f"Received {resp} instead of NACK")

    def create_normal_message(self, what: What | str) -> NormalMessage:
        """
        Create a normal message for the item.
        Args:
            what: The action to perform.
        Returns:
            A normal message.
        """
        if isinstance(what, str):
            what = What(what)

        return NormalMessage(
            (
                self._who,
                what,
                self._where
            )
        )

    def create_status_message(self) -> StatusRequest:
        """
        Create a status message for the item.

        Returns:
            A status message.
        """
        return StatusRequest(
            (
                self._who,
                self._where
            )
        )

    def create_dimension_writing_message(self, dimension: Dimension, *args: Value) -> DimensionWriting:
        """
        Create a dimension message for the item.
        Args:
            dimension: the dimension value to set.
            *args: the values to set.

        Returns:

        """
        # noinspection PyTypeChecker
        return DimensionWriting(
            (
                self._who,
                self._where,
                dimension,
                *args
            )
        )

    def create_dimension_request_message(self, dimension: Dimension) -> DimensionRequest:
        """
        Create a dimension request message for the item.
        Args:
            dimension: the dimension value to request.

        Returns:

        """
        return DimensionRequest(
            (
                self._who,
                self._where,
                dimension
            )
        )

    async def send_normal_message(self, what: What | str) -> None:
        """
        Send a normal message to the server and check the response.

        Args:
            what: The action to perform.

        Raises:
            RequestError: If the server does not acknowledge the message.
        """
        msg = self.create_normal_message(what)
        await self._send_message(msg)

        resp = await self._read_message()
        self._check_ack(resp)

    async def send_status_request(self) -> NormalMessage:
        """
        Send a status request to the server and check the response.

        Raises:
            RequestError: If the server does not acknowledge the message.
        """
        msg = self.create_status_message()
        await self._send_message(msg)

        resp = await self._read_message()
        self._check_nack(resp)

        ack = await self._read_message()
        self._check_ack(ack)

        if not isinstance(resp, NormalMessage):
            raise RequestError(f"Error sending message: {msg}, response: {ack}")

        return resp

    async def send_dimension_writing(self, dimension: Dimension | str, *args: Value) -> None:
        """
        Send a dimension writing message to the server and check the response.

        Args:
            dimension: the dimension value to set.
            *args: the values to set.

        Raises:
            RequestError: If the server does not acknowledge the message.
        """
        if isinstance(dimension, str):
            dimension = Dimension(dimension)

        msg = self.create_dimension_writing_message(dimension, *args)
        await self._send_message(msg)

        resp = await self._read_message()
        self._check_ack(resp)
