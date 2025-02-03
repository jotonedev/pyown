import asyncio
import logging

from pyown.client import Client
from pyown.messages import DimensionRequest, ACK, NACK
from pyown.tags import Who, Where, Dimension


async def run(host: str, port: int, password: str):
    client = Client(host=host, port=port, password=password)

    await client.start()

    # Get the ip address of the server
    await client.send_message(DimensionRequest((Who.GATEWAY, Where(), Dimension("10"))))

    # Parse response
    resp = None
    status = None
    try:
        resp = await client.read_message()
        if resp == NACK():
            logging.error("The server did not acknowledge the message")
            return await client.close()

        status = await client.read_message()
    except asyncio.TimeoutError:
        logging.error("Timeout while waiting for response")

    if status == ACK():
        logging.info("The server acknowledged the message")
        ip = resp.tags[-4:]
        print(f"The ip address of the server is {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}")
    else:
        logging.error("The server did not acknowledge the message")

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
    parser.add_argument(
        "--host", type=str, help="The host to connect to", default="192.168.1.35"
    )
    parser.add_argument(
        "--port", type=int, help="The port to connect to", default=20000
    )
    parser.add_argument(
        "--password",
        type=str,
        help="The password to authenticate with",
        default="12345",
    )

    args = parser.parse_args()

    main(args.host, args.port, args.password)
