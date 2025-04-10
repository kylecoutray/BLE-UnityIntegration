import sys
import asyncio
import struct
from bleak import BleakClient

#set the correct BLE device address and characteristic UUID
DEVICE_ADDRESS = "02:64:5C:8D:B0:56"
CHAR_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

#output file path where the new value overwrites the previous one
FILE_PATH = r"D:\GithubRepos\BLE-UnityIntegration\currentSpeed.txt"

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
