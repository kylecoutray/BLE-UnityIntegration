using UnityEngine;
using System;
using System.IO;

public class PlayerMovementFileRead : MonoBehaviour
{   
    private string filePath = @"D:\GithubRepos\BLE-UnityIntegration\currentSpeed.txt";
    
    //initialize all of our movement variables
    public float moveSpeed = 0f;
    public float speedFactor = 1f;
    public float interpolationRate = 2f;
    public float decelerationRate = 0.1f;
    public float lookSpeed = 0.2f;


    private CharacterController controller;
    private Vector3 moveDirection = Vector3.zero;
    private float rotationX = 0f;

// helper function to simplify things -- this function will return
// the updated speed, handling all movement properties
float UpdateMoveSpeed(float currentSpeed, float targetSpeed, float decelerationRate, float accelerationRate)
{
    // always apply deceleration, even when no update
    float newSpeed = Mathf.Max(0, currentSpeed - decelerationRate * Time.deltaTime);

    //if sensorSpeed indicates a lower speed than our current
    // ensure we don't overshoot the target by further decelerating at the constant rate.
    if (targetSpeed < newSpeed)
    {
        //decelerate further until we reach targetSpeed
        newSpeed = Mathf.Max(targetSpeed, newSpeed - decelerationRate * Time.deltaTime);
    }
    //if sensorSpeed is higher then our target speed
    // smoothly accelerate/interpolate toward that target
    else if (targetSpeed > newSpeed)
    {
        //linear interp. toward the target for smooth acceleration.
        newSpeed = Mathf.Lerp(newSpeed, targetSpeed, accelerationRate * Time.deltaTime);
    }

    return newSpeed;
}



    void Start()
    {
        controller = GetComponent<CharacterController>();
    }

    void Update()
    {
        float targetSpeed = 0f;

        try
            {
                //this reads cursor data from our file
                //adapted this from my other github repo: 
                // Dr.Constantinidis-PythonDS-Unity-Integration-Demo
                if (File.Exists(filePath))
                {
                    using (FileStream stream = new FileStream(filePath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                    using (StreamReader reader = new StreamReader(stream))
                    {
                        string data = reader.ReadToEnd().Trim();
                        if (!string.IsNullOrEmpty(data))
                        {
                            if(float.TryParse(data, out float sensorSpeed))
                            { 
                                targetSpeed = sensorSpeed * speedFactor;
                                Debug.Log($"Sensor Speed: {sensorSpeed:F2} m/s, Target Speed: {targetSpeed:F2} m/s");
                            }
                        }   
                    }
                }
            }
            catch (Exception ex)
            {
                Debug.LogError("Error reading file: " + ex.Message);
            }


        //wrote a function to update the move speed more accurately to a bike
        moveSpeed = UpdateMoveSpeed(moveSpeed, targetSpeed, decelerationRate, interpolationRate);



        /* move forward when W is pressed
        if (Input.GetKey(KeyCode.W))
        {
            moveDirection = transform.forward * moveSpeed;
        }
        else
        {
            moveDirection = Vector3.zero;
        }
        */

        //auto movement
        moveDirection = transform.forward * moveSpeed;

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

