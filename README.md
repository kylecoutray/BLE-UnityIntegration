# BLE-UnityIntegration

Phase 1:
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


