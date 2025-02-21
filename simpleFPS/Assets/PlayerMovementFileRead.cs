using UnityEngine;
using System;
using System.IO;

public class PlayerMovementFileRead : MonoBehaviour
{

    private string filePath = @"D:\GithubRepos\BLE-UnityIntegration\currentSpeed.txt";

    public float moveSpeed = 0f;
    public float lookSpeed = 2f;

    private CharacterController controller;
    private Vector3 moveDirection = Vector3.zero;
    private float rotationX = 0f;

    void Start()
    {
        controller = GetComponent<CharacterController>();
    }

    void Update()
    {
        try
            {
                //this reads cursor data from our file
                if (File.Exists(filePath))
                {
                    using (FileStream stream = new FileStream(filePath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                    {
                        using (StreamReader reader = new StreamReader(stream))
                        {
                            string data = reader.ReadToEnd().Trim();

                            if (!string.IsNullOrEmpty(data))
                            {
                                float.TryParse(data, out float x); 
                                Debug.Log($"Current Speed = {x}");
                                moveSpeed = x;
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Debug.LogError("Error reading file: " + ex.Message);
            }
        

        // move forward when W is pressed
        if (Input.GetKey(KeyCode.W))
        {
            moveDirection = transform.forward * moveSpeed;
        }
        else
        {
            moveDirection = Vector3.zero;
        }

        // apply movement
        controller.Move(moveDirection * Time.deltaTime);

        // handle looking around
        float lookX = Input.GetAxis("Horizontal") * lookSpeed; // Left/Right Arrow
        float lookY = Input.GetAxis("Vertical") * lookSpeed;   // Up/Down Arrow

        // rotate left/right
        transform.Rotate(0, lookX, 0);

        // tilt up/down (clamping to avoid flipping)
        rotationX -= lookY;
        rotationX = Mathf.Clamp(rotationX, -80f, 80f);
        Camera.main.transform.localRotation = Quaternion.Euler(rotationX, 0, 0);


    }
}

