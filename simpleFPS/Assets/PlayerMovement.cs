using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public float moveSpeed = 3f;
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
        // Move forward when W is pressed
        if (Input.GetKey(KeyCode.W))
        {
            moveDirection = transform.forward * moveSpeed;
        }
        else
        {
            moveDirection = Vector3.zero;
        }

        // Apply movement
        controller.Move(moveDirection * Time.deltaTime);

        // Handle looking around
        float lookX = Input.GetAxis("Horizontal") * lookSpeed; // Left/Right Arrow
        float lookY = Input.GetAxis("Vertical") * lookSpeed;   // Up/Down Arrow

        // Rotate left/right
        transform.Rotate(0, lookX, 0);

        // Tilt up/down (clamping to avoid flipping)
        rotationX -= lookY;
        rotationX = Mathf.Clamp(rotationX, -80f, 80f);
        Camera.main.transform.localRotation = Quaternion.Euler(rotationX, 0, 0);
    }
}
