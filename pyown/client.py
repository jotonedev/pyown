import asyncio
from asyncio import StreamReader, StreamWriter

from typing import Final, Literal

from pyown.message import *
from .auth.open import ownCalcPass


__all__ = ["OWNClient"]


# Use for sending commands and getting responses from the gateway
COMMAND_SESSION: Final = "9"
# Get every event from the gateway
# Use only for receiving events, not for sending commands
EVENT_SESSION: Final = "1"


class OWNClient:
    def __init__(self, host: str, port: str | int, password: str | int):
        """
        Initialize the OpenWebNet client.
        :param host: the IP address of the openwebnet gateway.
        :param port: the port of the openwebnet gateway.
        :param password: the password used to connect to the openwebnet gateway.
        """
        self.host = host
        self.port = port if isinstance(port, int) else int(port)
        self.password = password if isinstance(password, int) else int(password)

        self.reader: None | StreamReader = None
        self.writer: None | StreamWriter = None

    async def connect(self, session_type: Literal["9", "1"] = COMMAND_SESSION):
        self.reader, self.writer = await asyncio.open_connection(
            host=self.host,
            port=self.port,
            ssl=False,  # OpenWebNet does not support SSL
        )
        # Receive the initial ACK
        msg = await self.recv()
        if msg != ACK:
            raise ConnectionError(f"Unexpected response: {msg}")
        # Send the session type
        await self.send(RawMessage(tags=["99", session_type]))
        
    async def _open_auth(self, msg: OWNMessage):
        """
        Implement the OPEN algorithm for authentication.
        This is used in the majority of the cases.
        """
        # Receive the nonce
        msg = await self.recv()
        nonce = msg.tags[0].removeprefix("#")
        # Calculate the password
        password = ownCalcPass(self.password, nonce)
        # Send the password
        await self.send(RawMessage(tags=["#" + password]))
        # Receive the response
        try:
            msg = await self.recv(timeout=3)
        except asyncio.TimeoutError:
            raise ConnectionError("Authentication failed")
        # Check if the authentication was successful
        if msg == ACK:
            return
        elif msg == NACK:
            raise ConnectionError("Authentication failed")
        else:
            raise ConnectionError(f"Unexpected response: {msg}")

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

    async def _send(self, msg: str | bytes):
        """
        Send a message as it is to the openwebnet gateway.
        :param msg: the message to send
        """
        if isinstance(msg, str):
            msg = msg.encode()
        
        self.writer.write(msg)
        await self.writer.drain()

    async def _recv(self, timeout: int = 5, *, consume: bool = True) -> str:
        """
        Receive a single message from the openwebnet gateway.
        :param timeout: the maximum time to wait for the message
        :param consume: whether to consume the message from the buffer
        :return: the received message
        """
        # in openwebnet, messages starts with an asterisk
        # and end with two hashtags
        async with asyncio.timeout(timeout):
            if consume:
                msg = await self.reader.readuntil(b"##")
            else:
                msg = await self.reader.readuntil(b"##", 1024)
            
        return msg.decode(errors="ignore", encoding="ascii")  # omw uses only ascii characters

    async def send(self, msg: OWNMessage):
        """
        Send a message to the openwebnet gateway.
        :param msg: the message to send
        """
        msg = str(msg)
        await self._send(msg)

    async def recv(self, timeout: int = 5) -> OWNMessage:
        """
        Receive a message from the openwebnet gateway.
        :param timeout: the maximum time to wait for the message
        :return: the received message
        """
        return RawMessage.parse(await self._recv(timeout=timeout))
