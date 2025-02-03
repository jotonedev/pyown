import asyncio
import logging

from pyown import Client
from pyown.items import Light
from pyown.client import SessionType

log = logging.getLogger(__name__)


async def on_light_state_change(light: Light, state: bool):
    if state:
        log.info(f"Light at {light.where} is now on")
    else:
        log.info(f"Light at {light.where} is now off")


# noinspection DuplicatedCode
async def run(host: str, port: int, password: str):
    client = Client(
        host=host, port=port, password=password, session_type=SessionType.EventSession
    )

    Light.on_status_change(on_light_state_change)

    await client.start()
    await client.loop()


# noinspection DuplicatedCode
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
