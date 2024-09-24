import argparse
import asyncio

from .client import OWNClient


async def main(host: str, port: int, password: int) -> None:
    """Run the OpenWebNet client."""
    client = OWNClient(host, port, password)
    await client.connect()

    print(f"Connected to {host}:{port}")

    await client.close()
    print("Disconnected")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenWebNet client")
    parser.add_argument("--host", type=str, help="The OpenWebNet gateway IP address", default="192.168.0.120")
    parser.add_argument("--port", type=int, help="The OpenWebNet gateway port", default=20000)
    parser.add_argument("--password", type=str, help="The OpenWebNet gateway password", default="12345")
    args = parser.parse_args()

    asyncio.run(main(args.host, args.port, args.password))
