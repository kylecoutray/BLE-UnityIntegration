import asyncio
from bleak import BleakScanner

# simple scanner to find all BLE device addressses nearby and their name
async def scan_devices():
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"Name: {d.name}, Address: {d.address}")

if __name__ == "__main__":
    asyncio.run(scan_devices())
