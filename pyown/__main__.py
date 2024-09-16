import asyncio
import argparse

from tqdm import tqdm

from .client import OWNClient
from .message import *
from .constants.who import *


def build_active_power_request(device: str) -> RawMessage:
    """Build the active power request message."""
    return RawMessage(["#" + ENERGY_MANAGEMENT, device, "113"])


async def main(host: str, port: int, password: int) -> None:
    """Run the OpenWebNet client."""
    client = OWNClient(host, port, password)
    await client.connect()

    
    print(f"Connected to {host}:{port}")

    # Scan the OpenWebNet bus for energy management devices
    while True:
        await asyncio.sleep(0.5)
        print()
        try:
            for i in range(1, 4):
                who = f"5{i}"
                
                message = build_active_power_request(who)
                await client.send(message)
                response = await client.recv()

                if response == ACK:
                    continue

                if await client.recv() != ACK:
                    continue

                device = int(response.tags[-3])
                power = int(response.tags[-1])

                print(f"Device: {device}, Power: {power}W")
        except KeyboardInterrupt:
            break

    await client.close()
    print("Disconnected")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenWebNet client")
    parser.add_argument("--host", type=str, help="The OpenWebNet gateway IP address", default="192.168.0.120")
    parser.add_argument("--port", type=int, help="The OpenWebNet gateway port", default=20000)
    parser.add_argument("--password", type=str, help="The OpenWebNet gateway password", default="12345")
    args = parser.parse_args()
    
    asyncio.run(main(args.host, args.port, args.password))