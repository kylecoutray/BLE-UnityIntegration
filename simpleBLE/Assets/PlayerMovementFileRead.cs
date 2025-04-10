using UnityEngine;
using System;
using System.IO;

public class PlayerMovementFileRead : MonoBehaviour
{   
    // File path to the sensor speed file
    private string filePath = @"/Users/kyle./Documents/GitHub/BLE-UnityIntegration/currentSpeed.txt";
    
    // Movement variables
    public float moveSpeed = 0f;
    public float speedFactor = 1f; // (Unused currently but available if needed)
    public float lookSpeed = 0.2f;

    // Internal movement variables
    private CharacterController controller;
    private Vector3 moveDirection = Vector3.zero;
    private float rotationX = 0f;

    // Variable to store speed read from the file (sensor speed)
    private float sensorSpeed = 0f;

    void Start()
    {
        controller = GetComponent<CharacterController>();
    }

    void Update()
    {
        // Read sensorSpeed from the file
        try
        {
            if (File.Exists(filePath))
            {
                using (FileStream stream = new FileStream(filePath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                using (StreamReader reader = new StreamReader(stream))
                {
                    string data = reader.ReadToEnd().Trim();
                    if (!string.IsNullOrEmpty(data))
                    {
                        if (float.TryParse(data, out float newSensorSpeed))
                        {
                            sensorSpeed = newSensorSpeed;
                            Debug.Log($"Sensor Speed: {sensorSpeed:F2} m/s");
                        }
                    }
                }
            }
        }
        catch (Exception ex)
        {
            Debug.LogError("Error reading file: " + ex.Message);
        }

        // Use sensorSpeed to update moveSpeed directly
        moveSpeed = sensorSpeed;

        // Auto movement based on the sensorSpeed
        moveDirection = transform.forward * moveSpeed;
        controller.Move(moveDirection * Time.deltaTime);

        // Handle camera rotation (horizontal and vertical remain unchanged)
        float lookX = Input.GetAxis("Horizontal") * lookSpeed; // Left/Right Arrow
        float lookY = Input.GetAxis("Vertical") * lookSpeed;   // Up/Down Arrow

        // Rotate left/right
        transform.Rotate(0, lookX, 0);

        // Tilt up/down (clamp to avoid flipping)
        rotationX -= lookY;
        rotationX = Mathf.Clamp(rotationX, -80f, 80f);
        Camera.main.transform.localRotation = Quaternion.Euler(rotationX, 0, 0);
    }
}
