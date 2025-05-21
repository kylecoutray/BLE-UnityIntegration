# BLE-UnityIntegration

This project uses BLE devices to control a Unity camera in real time. The system evolved through three phases:

Phase I: Garmin Speed Sensor

Phase II: Single Arduino Nano BLE

Phase III: Dual Arduino Nanos for differential steering and speed

--------------------------------------------------------------------------------------



**Phase 1:**
  This project is to connect to a Garmin Speed Sensor 2 through BLE and parse the real time speed from the CSC data stream to manipulate a Unity environment.
  
  I am utilizing the bleak and asyncio library. 
  
  You must do `pip install bleak` for the following scripts to run.
  
  1) run `bleakScanner.py` to look for device (to find bluetooth address)
  2) run `gattServices.py` to see the services available to subscribe to
  3) run `batteryLevel.py` to see battery level (not verified if this is accurate)
  4) run `speedNotification.py` to get live updates of the speed (estimated in m/s)
  
  **To run the Unity Scene properly:**
  1) Fix all file paths on local machine
  2) Turn on Speed Sensor 2 (Rotate until lights flash)
  3) Run `speedNotification.py`
  4) Enter ` "y" ` when prompted
  5) Run Unity simpleBLE "barebones" scene
  
  Control camera with arrow keys, camera will accelerate based on speed sensor.
  
  Let me know if you have any issues or questions :)
  
  view the current state here:
  `<<(Click the thumbnail below)>>`

  
  [![See the current state here.](https://img.youtube.com/vi/C9kRAWhEDl0/0.jpg)](https://youtu.be/C9kRAWhEDl0)




**PHASE 2 (The better version) Utilizing Arduino Nanos and BLE**

View the current state here:
https://youtu.be/JC-IjKi16ps
https://youtu.be/JC-IjKi16ps
https://youtu.be/JC-IjKi16ps
[![See the current state here.](https://img.youtube.com/vi/JC-IjKi16ps/0.jpg)](https://youtu.be/JC-IjKi16ps)



## 🔴 Phase III: Dual Arduino Nano BLE – Differential Control

Phase III introduces **two Arduino Nano 33 BLE Sense boards**, simulating left and right wheel speeds for advanced motion control.

### Logic Enhancements

* **Angle** = Difference between left/right speeds
* **Forward Speed** = Average of both speeds
* **Sliding Factor** = Controls how sharply angle changes

[![📹 Watch Phase III Demo](https://img.youtube.com/vi/ZU_S5mPfqVU/0.jpg)](https://www.youtube.com/shorts/ZU_S5mPfqVU)


---

## 📜 How to Use (Phase III)

### 1. **Run Arduino Sketch**

* Upload `nanoBLE.ino` to each Nano
* **Important**: Edit line 24 to label each device as `"leftNanoSense"` or `"rightNanoSense"`

### 2. **Find BLE Addresses**

* Run `bleakScanner.py`
* Locate both `leftNanoSense` and `rightNanoSense`
* Save their addresses

### 3. **Start Dual BLE Read**

* Run `doubleNanoBLEread.py`
* This script:

  * Connects to both Nanos
  * Writes speed data to `currentSpeedLeft.txt` and `currentSpeedRight.txt`
* **Check config**:

  * Correct BLE addresses
  * Valid characteristic UUID
  * Valid file paths for output

### 4. **Launch Unity Scene**

* Unity reads from the speed files to simulate motion
* Steering and speed are determined live

---

## 📁 Files of Interest

| File                                             | Description                                        |
| ------------------------------------------------ | -------------------------------------------------- |
| `nanoBLE.ino`                                    | Arduino sketch for broadcasting speed over BLE     |
| `doubleNanoBLEread.py`                           | Connects to two Nanos, writes speeds to text files |
| `currentSpeedLeft.txt` / `currentSpeedRight.txt` | Real-time outputs for Unity input                  |
| `PlayerMovement.cs`                              | Unity script for camera movement based on input    |
| `instructions.txt`                               | Step-by-step Phase III guide                       |
| `bleakScanner.py`                                | Find BLE device addresses                          |
| `speedNotification.py`                           | Legacy Garmin speed reader                         |
| `batteryLevel.py`                                | Optional battery check                             |
| `gattServices.py`                                | View GATT services on BLE devices                  |

---

