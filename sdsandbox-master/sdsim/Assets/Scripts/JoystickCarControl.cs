using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityStandardAssets.CrossPlatformInput;

public class JoystickCarControl : MonoBehaviour 
{
	public GameObject carObj;
	private ICar car;

	public float MaximumSteerAngle = 1.0f; //has to be kept in sync with the car, as that's a private var.
	
	void Awake()
	{
		if(carObj != null)
			car = carObj.GetComponent<ICar>();
	}

	private void FixedUpdate()
	{

        int steer;
        // pass the input to the car!
        float h = CrossPlatformInputManager.GetAxis("Horizontal") * MaximumSteerAngle;
        if (h > .5)
            steer = 5;
        else if (h < -.5)
            steer = -5;
        else
            steer = 0;
        // pass the input to the car!
        //float h = CrossPlatformInputManager.GetAxis("Horizontal");
		float v = CrossPlatformInputManager.GetAxis("Vertical");
		float handbrake = CrossPlatformInputManager.GetAxis("Jump");
        bool handbrake1 = CrossPlatformInputManager.GetButton("xBoxA");
		car.RequestSteering(steer);
		car.RequestThrottle(v * 90);
        car.RequestFootBrake(handbrake);
        if (handbrake1)
        {
            print("HIT ME");
            car.RequestThrottle(0f);
            car.RequestFootBrake(1f);
            
        }
        else
            car.RequestFootBrake(0);
        
        
    }
}
