import sys
import asyncio
from bleak import BleakClient

# put your BLE address and desired characteristic below
DEVICE_ADDRESS = "F8:BC:3D:C6:AD:0D"
CSC_MEASUREMENT_UUID = "00002a5b-0000-1000-8000-00805f9b34fb"
# in our case we want the cadence and speed sensor
# 0x2A5B provides the wheel(speed) and crank(cadence) data
# it sends the data as raw revolution counts and timestamps
# we must calculate speed by comparing consecutive measurements.


# wheel circumference (in meters) ~ 2.1 average. 
# this may also serve as a scale factor later for Unity implementation
WHEEL_CIRCUMFERENCE_M = 2.1

# keep track of the previous measurement for deltas
prev_wheel_revs = None
prev_wheel_time = None  

WRITE_OUTPUT = False

#opens our file for writing speed data
output_file = open("D:\GithubRepos\ANT-UnityIntegration\currentSpeed.txt", "w")


def parse_csc_measurement(data: bytearray):
    """
    data: raw notification payload (bytearray)
    Returns a dict with the parsed values (None if not present).
    The bytearray will be in the following format:
    Flags (1 byte) | Wheel Revs (4 bytes) | Wheel Time (2 bytes) | Crank Revs (2 bytes) | Crank Time (2 bytes)

    """
    flags = data[0]
    index = 1

    wheel_revolutions = None
    wheel_event_time = None
    crank_revolutions = None
    crank_event_time = None

    # if wheel revolution Data is present (bit 0)
    if flags & 0x01:
        # 4 bytes: cumulative wheel revolutions (uint32)
        wheel_revolutions = int.from_bytes(data[index:index+4], byteorder='little')
        index += 4
        # 2 bytes: last wheel event time (uint16)
        wheel_event_time = int.from_bytes(data[index:index+2], byteorder='little')
        index += 2

    # if crank revolution data is present (bit 1)
    if flags & 0x02:
        # 2 bytes: cumulative crank Revolutions (uint16)
        crank_revolutions = int.from_bytes(data[index:index+2], byteorder='little')
        index += 2
        # 2 bytes: last crank event time (uint16)
        crank_event_time = int.from_bytes(data[index:index+2], byteorder='little')
        index += 2

    return {
        "wheel_revolutions": wheel_revolutions,
        "wheel_event_time": wheel_event_time,
        "crank_revolutions": crank_revolutions,
        "crank_event_time": crank_event_time,
    }


def notification_handler(sender, data):
    global prev_wheel_revs, prev_wheel_time

    parsed = parse_csc_measurement(data)
    wr = parsed["wheel_revolutions"]
    wt = parsed["wheel_event_time"]

    if wr is not None and wt is not None:
        if prev_wheel_revs is not None and prev_wheel_time is not None:
            delta_revs = wr - prev_wheel_revs
            delta_time = wt - prev_wheel_time

            if delta_time > 0 and delta_revs >= 0:
                # convert delta_time from 1/1024s to seconds
                time_seconds = delta_time / 1024.0
                distance_m = delta_revs * WHEEL_CIRCUMFERENCE_M
                speed_m_s = distance_m / time_seconds
                print(f"Speed: {speed_m_s:.2f} m/s")
                if WRITE_OUTPUT:
                    output_file.seek(0)  #reset file to overwrite
                    output_file.write(f"{speed_m_s:.2f}") #writes our speed
                    output_file.flush()  #write data immediately 


        # update previous measurement
        prev_wheel_revs = wr
        prev_wheel_time = wt

async def main():
    global WRITE_OUTPUT
    #prompt if user wants to write the speed data to file
    response = input("Would you like to write the speed data to an output file? (y/n): ")
    
    #update global var for our if statement inside notification_handler
    WRITE_OUTPUT = response.strip().lower().startswith('y')

    async with BleakClient(DEVICE_ADDRESS) as client:
        await client.start_notify(CSC_MEASUREMENT_UUID, notification_handler)
        print("Subscribed to CSC Measurement notifications. Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(1) #this is just so we aren't busy waiting. reduces CPU usage if there's no update
        except KeyboardInterrupt:
            print("Stopping notifications.")
        finally:
            await client.stop_notify(CSC_MEASUREMENT_UUID)

if __name__ == "__main__":
    asyncio.run(main())
