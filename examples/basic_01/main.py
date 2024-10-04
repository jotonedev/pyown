import asyncio
import logging

from pyown.client.base import BaseClient
from pyown.messages import MessageType, DimensionRequest
from pyown.tags import Who, Where, Dimension


async def run(host: str, port: int, password: str):
    client = BaseClient(
        host=host,
        port=port,
        password=password
    )

    await client.start()

    # Get the ip address of the server
    resp = await client.send_message_with_response(
        DimensionRequest(
            (
                Who.GATEWAY,
                Where(),
                Dimension("10")
            )
        )
    )
    for msg in resp:
        if msg.type == MessageType.NACK:
            print("The server did not accept the request")
            return
        else:
            if msg.type == MessageType.ACK:
                print(f"The server accepted the request")
            else:
                ip = msg.tags[-4:]
                print(f"The ip address of the server is {ip}")

    await client.close()


def main(host: str, port: int, password: str):
    # Set the logging level to DEBUG
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Run the asyncio event loop
    asyncio.run(run(host, port, password))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, help="The host to connect to", default="192.168.1.35")
    parser.add_argument("--port", type=int, help="The port to connect to", default=20000)
    parser.add_argument("--password", type=str, help="The password to authenticate with", default="12345")

    args = parser.parse_args()

    main(args.host, args.port, args.password)
