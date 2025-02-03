import asyncio
import logging

from pyown.client import Client
from pyown.items.energy import EnergyManagement


async def run(host: str, port: int, password: str):
    client = Client(
        host=host,
        port=port,
        password=password,
    )

    await client.start()

    f520 = EnergyManagement(
        where="51",
        client=client,
    )

    power = await f520.get_active_power()
    logging.info(f"Active power: {power}")

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
