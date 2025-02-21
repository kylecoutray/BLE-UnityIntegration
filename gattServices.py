import asyncio
from bleak import BleakClient

#use your own ble address. find it with bleakScanner.py if you need
DEVICE_ADDRESS = "F8:BC:3D:C6:AD:0D"

async def list_services():
    async with BleakClient(DEVICE_ADDRESS) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid} - {service.description}") #prints all services
            for char in service.characteristics: #prints all characteristics for each service
                print(f"  Characteristic: {char.uuid} - {char.description}")

if __name__ == "__main__":
    asyncio.run(list_services())
