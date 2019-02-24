import socketio
from picamera import PiCamera
import time
import base64
from io import BytesIO
from MotorInterface import MotorInterface as Motor
from AccelInterface import AccelInterface as Accel
import csv
import datetime

camera = PiCamera()
camera.resolution = (160, 120)
# camera.shutter_speed = 800
# camera.framerate = 900
# camera.video_stabilization = True
my_stream = BytesIO()
sleep(2)
start = time.time()
for i in range(5000):
    # sleep(0.5)
    print("help-"+str(i))
    data =	{
        "steering_angle": 0,
        "throttle": 90,
        "speed": 90,
        "image": camera.capture(my_stream, 'jpeg', use_video_port=True)
    }
    if time.time() - start > 30:
        break
    my_stream.seek(0)
    my_stream.truncate()
    # camera.capture(my_stream, 'jpeg')
    # camera.capture('/home/pi/Documents/AI/img/test%s.jpg' % i)
