import asyncio
import logging

from pyown.client import Client, SessionType
from pyown.items.automation import AutomationStatusEvent, WhatAutomation

log = logging.getLogger(__name__)


async def on_shutter_state_change(event: AutomationStatusEvent):
    """Log the new state of a shutter when it changes."""
    if event.state == WhatAutomation.UP:
        log.info(f"Shutter at {event.where} is now up")
    elif event.state == WhatAutomation.DOWN:
        log.info(f"Shutter at {event.where} is now down")
    elif event.state == WhatAutomation.STOP:
        log.info(f"Shutter at {event.where} is now stopped")


# noinspection DuplicatedCode
async def run(host: str, port: int, password: str):
    """Connect with an event session and listen for shutter state changes."""
    client = Client(host=host, port=port, password=password, session_type=SessionType.EventSession)

    client.events.subscribe(AutomationStatusEvent, on_shutter_state_change)

    await client.start()
    await client.loop()


def main(host: str, port: int, password: str):
    """Configure logging and run the async example."""
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
