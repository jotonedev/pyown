import asyncio
import logging

import datetime

from pyown.client import Client, SessionType
from pyown.items import Gateway, WhatGateway


async def on_time_change(gateway: Gateway, time: datetime.time):
    print(f"Time of the gateway is now {time}")


async def run(host: str, port: int, password: str):
    client = Client(
        host=host, port=port, password=password, session_type=SessionType.EventSession
    )

    Gateway.register_callback(WhatGateway.TIME, on_time_change)

    await client.start()
    await client.loop()


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
