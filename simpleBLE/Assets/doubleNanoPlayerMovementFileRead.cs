using UnityEngine;
using System;
using System.IO;

public class doubleNanoPlayerMovementFileRead : MonoBehaviour
{   
    private string filePathLeft = @"C:/Github/BLE-UnityIntegration/currentSpeedLeft.txt";
    private string filePathRight = @"C:/Github/BLE-UnityIntegration/currentSpeedRight.txt";

    public float moveSpeed = 0f;
    public float speedFactor = 1f;
    public float lookSpeed = 0.2f;
    public float tiltFactor = 1f;

    private CharacterController controller;
    private Vector3 moveDirection = Vector3.zero;
    private float rotationX = 0f;

    private float speedLeft = 0f;
    private float speedRight = 0f;

    void Start()
    {
        controller = GetComponent<CharacterController>();
    }

    void Update()
    {
        speedLeft = ReadSpeed(filePathLeft);
        speedRight = ReadSpeed(filePathRight);

        float avgSpeed = (speedLeft + speedRight) / 2f;
        float turnAmount = (speedLeft - speedRight) * tiltFactor;

        moveSpeed = avgSpeed;
        moveDirection = transform.forward * moveSpeed;
        controller.Move(moveDirection * Time.deltaTime);

        transform.Rotate(0, turnAmount * Time.deltaTime, 0);

        float lookX = Input.GetAxis("Horizontal") * lookSpeed;
        float lookY = Input.GetAxis("Vertical") * lookSpeed;

        transform.Rotate(0, lookX, 0);

        rotationX -= lookY;
        rotationX = Mathf.Clamp(rotationX, -80f, 80f);
        Camera.main.transform.localRotation = Quaternion.Euler(rotationX, 0, 0);
    }

    float ReadSpeed(string path)
    {
        try
        {
            if (File.Exists(path))
            {
                using (FileStream stream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                using (StreamReader reader = new StreamReader(stream))
                {
                    string data = reader.ReadToEnd().Trim();
                    if (!string.IsNullOrEmpty(data) && float.TryParse(data, out float speed))
                        return speed;
                }
            }
        }
        catch (Exception ex)
        {
            Debug.LogError("Error reading file: " + ex.Message);
        }
        return 0f;
    }
}
