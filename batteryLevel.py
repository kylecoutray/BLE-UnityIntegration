import asyncio
from bleak import BleakClient

#input your ble address. use bleakScanner.py to locate address
DEVICE_ADDRESS = "F8:BC:3D:C6:AD:0D"

#these are standard UUIDs for battery, but you can confirm with gattServices.py
BATTERY_SERVICE_UUID = "0000180f-0000-1000-8000-00805f9b34fb"
BATTERY_LEVEL_UUID   = "00002a19-0000-1000-8000-00805f9b34fb"

async def main():
    async with BleakClient(DEVICE_ADDRESS) as client:
        battery_data = await client.read_gatt_char(BATTERY_LEVEL_UUID)
        battery_level = int(battery_data[0])
        print(f"Battery Level: {battery_level}%")

if __name__ == "__main__":
    asyncio.run(main())
