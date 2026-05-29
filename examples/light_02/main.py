import asyncio
import logging

from pyown import Client
from pyown.client import SessionType
from pyown.items.lighting import LightStatusEvent

log = logging.getLogger(__name__)


async def on_light_state_change(event: LightStatusEvent):
    """Log the new state of a light when it changes."""
    if event.on:
        log.info(f"Light at {event.where} is now on")
    else:
        log.info(f"Light at {event.where} is now off")


# noinspection DuplicatedCode
async def run(host: str, port: int, password: str):
    client = Client(host=host, port=port, password=password, session_type=SessionType.EventSession)

    client.events.subscribe(LightStatusEvent, on_light_state_change)

    await client.start()
    await client.loop()


# noinspection DuplicatedCode
def main(host: str, port: int, password: str):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    asyncio.run(run(host, port, password))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, help="The host to connect to", default="192.168.1.35")
    parser.add_argument("--port", type=int, help="The port to connect to", default=20000)
    parser.add_argument(
        "--password",
        type=str,
        help="The password to authenticate with",
        default="12345",
    )

    args = parser.parse_args()

    main(args.host, args.port, args.password)
