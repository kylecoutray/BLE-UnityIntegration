import serial
import time

# === CONFIGURATION ===
PORT = "COM3"         # Replace with your Arduino COM port
BAUD_RATE = 115200
FILENAME = "curSpeed.txt"

# === START SERIAL CONNECTION ===
with serial.Serial(PORT, BAUD_RATE, timeout=1) as ser:
    print(f" Writing live data to: {FILENAME}")
    
    while True:
        try:
            line = ser.readline().decode(errors='ignore').strip()
            if line:
                with open(FILENAME, 'w', encoding='utf-8') as f:

                    f.write(line)
                print(f"[{time.time():.2f}] {line}")
        except KeyboardInterrupt:
            print("\nLogging stopped by user.")
            break
