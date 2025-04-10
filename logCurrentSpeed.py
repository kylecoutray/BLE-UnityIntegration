import serial
import os

COM_PORT = '/dev/cu.usbmodem1101'
BAUD_RATE = 9600

# Write to the same directory as the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'currentSpeed.txt')

def main():
    print(f"Will write to: {OUTPUT_FILE}")
    
    try:
        with serial.Serial(COM_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening on {COM_PORT}...")
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    #print(f"[SERIAL] {line}")
                    with open(OUTPUT_FILE, 'w') as f:
                        f.write(line)
                        f.flush()
                    #print(f"[FILE] Wrote: {line}")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == '__main__':
    main()
