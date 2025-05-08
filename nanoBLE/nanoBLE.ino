#include <ArduinoBLE.h>
#include <Arduino_BMI270_BMM150.h>

//define a custom BLE service UUID and a characteristic UUID.
BLEService sensorService("00000000-0000-0000-0000-000000000000");
BLECharacteristic gyroCharacteristic("00000000-0000-0000-0000-000000000001", BLERead | BLENotify, sizeof(float));


void setup() {
  Serial.begin(9600);
  //use this short delay instead of an indefinite wait so the code will proceed even without a USB connection
  delay(1000);

  // Initialize BLE
  if (!BLE.begin()) {
    Serial.println("BLE initialization failed!");
    while (1) {
      ; // Halt if BLE doesn't start
    }
  }
  
  //set BLE local name and advertise our custom service

  BLE.setLocalName("rightNanoSense");

  //uncomment this for right arduino
  //BLE.setLocalName("leftNanoSense");

  BLE.setAdvertisedService(sensorService);
  sensorService.addCharacteristic(gyroCharacteristic);
  BLE.addService(sensorService);
  
  //initialize characteristic with zero value
  float initialValue = 0;
  gyroCharacteristic.writeValue((byte *)&initialValue, sizeof(initialValue));
  
  // Start advertising so that a central can connect
  BLE.advertise();
  Serial.println("BLE device is now advertising");

  // Initialize the IMU sensor using the required library
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1) {
      ; //halt if the IMU is not available
    }
  }
  
  Serial.println("IMU initialized successfully");
}

void loop() {
  //check for BLE central connection
  BLEDevice central = BLE.central();
  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());
    
    // While the central is connected, continuously read sensor data and update the BLE characteristic
    while (central.connected()) {
      float ax, ay, az;   // Accelerometer data (don't need for this)
      float gx, gy, gz;   // Gyroscope data
      
      //check if sensor data is available
      if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
        //read acceleration (not used) and gyroscope data from the sensor
        IMU.readAcceleration(ax, ay, az);
        IMU.readGyroscope(gx, gy, gz);
        
        //calculate the magnitude of the gyroscope vector
        float gyroMagnitude = sqrt(gx * gx + gy * gy + gz * gz);
        
        //apply a threshold to filter out noise (threshold = 5)
        const float threshold = 5;
        if (gyroMagnitude < threshold) {
          gyroMagnitude = 0;
        }
        
        //compute the value without altering the original computation:
        float valueToSend = gyroMagnitude / 100;
        
        //send the value over BLE as a 4 byte float data
        gyroCharacteristic.writeValue((byte *)&valueToSend, sizeof(valueToSend));
        
        //also print to serial for debugging purposes -- only works if connected via USB
        Serial.println(valueToSend);
      }
      
      //short delay to allow sensor update and BLE notifications
      delay(100);
    }
    
    // Report when the central disconnects
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}
