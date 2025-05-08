import sys
import asyncio
import struct
from bleak import BleakClient

# BLE addresses (update LEFT_NANO_ADDRESS before running)
RIGHT_NANO_ADDRESS = "DF:5D:38:36:41:CC"
LEFT_NANO_ADDRESS = "XX:XX:XX:XX:XX:XX"  # <-- Replace with actual MAC address

# Shared characteristic UUID
CHAR_UUID = "00000000-0000-0000-0000-000000000001"

# Output files
FILE_PATH_LEFT = r"C:/Github/BLE-UnityIntegration/currentSpeedLeft.txt"
FILE_PATH_RIGHT = r"C:/Github/BLE-UnityIntegration/currentSpeedRight.txt"

def make_notification_handler(file_path, label):
    def handler(sender, data: bytearray):
        try:
            speed_value = struct.unpack('f', data)[0]
            with open(file_path, "w") as output_file:
                output_file.write(f"{speed_value:.2f}")
            print(f"{label} Speed updated: {speed_value:.2f}")
        except Exception as e:
            print(f"Error processing {label} notification:", e)
    return handler

async def handle_device(address, label, file_path):
    async with BleakClient(address) as client:
        print(f"Connected to {label} ({address})")
        handler = make_notification_handler(file_path, label)
        await client.start_notify(CHAR_UUID, handler)
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            await client.stop_notify(CHAR_UUID)
            print(f"{label} notifications stopped")

async def main():
    tasks = [
        asyncio.create_task(handle_device(RIGHT_NANO_ADDRESS, "Right", FILE_PATH_RIGHT)),
        asyncio.create_task(handle_device(LEFT_NANO_ADDRESS, "Left", FILE_PATH_LEFT)),
    ]
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        for task in tasks:
            task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
