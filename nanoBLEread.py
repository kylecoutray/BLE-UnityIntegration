import sys
import asyncio
import struct
from bleak import BleakClient


DEVICE_ADDRESS = "DF:5D:38:36:41:CC"
CHAR_UUID = "00000000-0000-0000-0000-000000000001"

#output file path where the new value overwrites the previous one
FILE_PATH = r"C:/Github/BLE-UnityIntegration/currentSpeed.txt"

def notification_handler(sender, data: bytearray):
    """
    Callback for BLE notifications.
    Unpacks a float from 4 bytes of data and overwrites the output file.
    """
    try:
        speed_value = struct.unpack('f', data)[0]
        with open(FILE_PATH, "w") as output_file:
            output_file.write(f"{speed_value:.2f}")
        print(f"Speed updated: {speed_value:.2f}")
    except Exception as e:
        print("error processing notification:", e)

async def main():
    async with BleakClient(DEVICE_ADDRESS) as client:
        print(f"Connected to {DEVICE_ADDRESS}")
        await client.start_notify(CHAR_UUID, notification_handler)
        print("subbed to notifications. ctrl + C to stop")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("notifications stopped")
        finally:
            await client.stop_notify(CHAR_UUID)

if __name__ == "__main__":
    asyncio.run(main())
