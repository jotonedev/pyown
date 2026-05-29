import asyncio
import logging

from pyown.client import Client, SessionType
from pyown.events import Event
from pyown.items.gateway import GatewayTimeEvent


async def on_time_change(event: GatewayTimeEvent):
    """Print the gateway's time when it changes."""
    print(f"Time of the gateway is now {event.time}")


async def on_any_event(event: Event):
    """Catch-all for debugging: log every event the gateway emits."""
    print(f"event: {type(event).__name__} where={event.where} payload={event!r}")


async def run(host: str, port: int, password: str):
    """Connect with an event session and listen for gateway time changes."""
    client = Client(host=host, port=port, password=password, session_type=SessionType.EventSession)

    client.events.subscribe(GatewayTimeEvent, on_time_change)
    # Demonstrate the catch-all path; comment out for less verbose output.
    client.events.subscribe_all(on_any_event)

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
