#include <Arduino_BMI270_BMM150.h>

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for Serial to initialize
  }
  
  // Initialize the IMU sensor
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1) {
      ; // Halt if the IMU is not available
    }
  }
  
  Serial.println("IMU initialized successfully");
}

void loop() {
  float ax, ay, az;   // Accelerometer data (if needed for further processing)
  float gx, gy, gz;   // Gyroscope data
  
  // Check if sensor data is available
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
    IMU.readAcceleration(ax, ay, az); // Read acceleration (not directly used here)
    IMU.readGyroscope(gx, gy, gz);      // Read gyroscope data
    
    // Calculate the magnitude of the gyroscope vector
    float gyroMagnitude = sqrt(gx * gx + gy * gy + gz * gz);
    
    // Apply a threshold filter to eliminate resting noise (e.g., 0.26 when idle)
    const float threshold = 5;  // Adjust threshold as needed based on testing
    if (gyroMagnitude < threshold) {
      gyroMagnitude = 0;
    }
    
    // Print the computed speed metric to the serial console
    
    Serial.println(gyroMagnitude/100);
  }
  
  // Short delay to allow for sensor update
  delay(100);
}
