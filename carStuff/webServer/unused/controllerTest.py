#import evdev
from evdev import InputDevice, categorize, ecodes
import os
from MotorInterface import MotorInterface as Motor

MC = Motor()

#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event0')

MAX_VALUE_JOYSTICK = 65535

MAX_VALUE_TRIGGER = 1023

TYPE_AXIS = 3

TYPE_BUTTON = 1

LEFT_STICK_X_AXIS = 0

LEFT_STICK_Y_AXIS = 1

TRIGGER_LEFT = 10

TRIGGER_RIGHT = 9

BUTTON_X = 307

BUTTON_A = 304

BUTTON_Y = 308

BUTTON_B = 305

BUTTON_LB = 310

BUTTON_RB = 311

MIN_THROTTLE = 90

MAX_THROTTLE = 255

THROTTLE_SCALER = (MAX_THROTTLE-MIN_THROTTLE)/2

xAxis = MAX_VALUE_JOYSTICK/2

JOYSTICK_ALLOWANCE = 10000

LEFT_TURN = (MAX_VALUE_JOYSTICK/2)-JOYSTICK_ALLOWANCE

RIGHT_TURN = (MAX_VALUE_JOYSTICK/2)+JOYSTICK_ALLOWANCE

leftTriggerThrottleAddition =0

rightTriggerThrottleAddition =0

accelPressed = False

reversePressed = False

direction = 0

throttle = 0
#prints out device info at start
print(gamepad)


#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():

    # print("type:",event.type)
    # print("code:",event.code)
    # print("value:",event.value)
    if event.type == TYPE_AXIS:
        # Axis have value of 0 (left or up) to MAX_VALUE_<type> (right or down) 
        # Left Stick
        if (event.code == LEFT_STICK_X_AXIS or event.code == LEFT_STICK_Y_AXIS):
            #x axis
            if event.code == LEFT_STICK_X_AXIS:
                xAxis = event.value
            #y axis
            if event.code == LEFT_STICK_X_AXIS:
                yAxis = event.value
        if (event.code == TRIGGER_LEFT):
            leftTriggerThrottleAddition = (event.value/MAX_VALUE_TRIGGER)*THROTTLE_SCALER
        if (event.code == TRIGGER_RIGHT):
            rightTriggerThrottleAddition = (event.value/MAX_VALUE_TRIGGER)*THROTTLE_SCALER
  
    elif event.type == TYPE_BUTTON:
        # buttons have a value of one to zero
        if event.code == BUTTON_A:
            if event.value == 0:
                accelPressed = False
            if event.value == 1:
                accelPressed = True
        if event.code == BUTTON_X:
            if event.value == 0:
                reversePressed = False
            if event.value == 1:
                reversePressed = True

    if accelPressed:
        throttle = MIN_THROTTLE+leftTriggerThrottleAddition+rightTriggerThrottleAddition
    elif reversePressed:
        throttle = (MIN_THROTTLE+leftTriggerThrottleAddition+rightTriggerThrottleAddition)*-1
    else:
        throttle = 0

    if xAxis > RIGHT_TURN:
        direction = 1
    elif xAxis < LEFT_TURN:
        direction = -1
    else:
        direction = 0
    

    print("throttle",throttle)
    print("direction",direction)
    MC.setThrottle(throttle)
    MC.setSteering(direction)
    # print(categorize(event))
