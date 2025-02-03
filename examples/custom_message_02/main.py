import asyncio
import logging

from pyown.client import Client
from pyown.messages import DimensionRequest, ACK, NACK, DimensionResponse
from pyown.tags import Who, Where, Dimension


async def run(host: str, port: int, password: str):
    client = Client(host=host, port=port, password=password)

    await client.start()

    # Request the 7 october energy management data
    await client.send_message(
        DimensionRequest((Who.ENERGY_MANAGEMENT, Where("52"), Dimension("511#10#7")))
    )

    while True:
        try:
            resp = await client.read_message()
        except asyncio.TimeoutError:
            logging.error("Timeout")
            break

        # ACK is the last message
        if isinstance(resp, ACK):
            break
        elif isinstance(resp, NACK):
            logging.error("Received NACK")
        elif isinstance(resp, DimensionResponse):
            logging.info(f"Received response: {resp}")
            print(resp.dimension.parameters)
            month = resp.dimension.parameters[0]
            day = resp.dimension.parameters[1]
            tag = resp.values[0]
            value = resp.values[1]
            logging.info(
                f"Month: {month}, Day: {day}, Number of the measure: {tag}, Value: {value}"
            )

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
