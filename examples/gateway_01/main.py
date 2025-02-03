import asyncio
import logging

from pyown.client import Client
from pyown.items import Gateway


async def run(host: str, port: int, password: str):
    client = Client(
        host=host,
        port=port,
        password=password,
    )

    await client.start()

    gateway = Gateway(client=client)

    # get ip address of the gateway
    ip = await gateway.get_ip()
    print(ip)

    # get the model of the gateway
    model = await gateway.get_model()
    print(model.name)

    # get datetime of the gateway
    datetime = await gateway.get_datetime()
    print(datetime)

    # get the kernel version of the gateway
    kernel = await gateway.get_kernel_version()
    print(kernel)

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
