# BLE-UnityIntegration
This project is to connect to a Garmin Speed Sensor 2 through BLE and parse the real time speed from the CSC data stream to manipulate a Unity environment.

I am utilizing the bleak and asyncio library. 

You must do 'pip install bleak' to use bleakScanner

1) run 'bleakScanner.py' to look for device (to find bluetooth address)
2) run 'gattServices.py' to see the services available to subscribe to
3) run 'batteryLevel.py' to see battery level (not verified if this is accurate)
4) run 'speedNotification.py' to get live updates of the speed (estimated in m/s)

Let me know if you have any issues or questions :)

