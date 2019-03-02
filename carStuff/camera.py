import socketio
from picamera import PiCamera
import time
import base64
from io import BytesIO
from MotorInterface import MotorInterface as Motor
from AccelInterface import AccelInterface as Accel
import csv
import datetime
import numpy as np

camera = PiCamera()
camera.resolution = (160, 120)
# camera.shutter_speed = 800

# camera.framerate = 90

# camera.video_stabilization = True
# my_stream = BytesIO()
my_stream = np.empty((240, 320, 3), dtype=np.uint8)
time.sleep(1)
start = time.time()
for i in range(5000):
    # sleep(0.5)
    

    start2 = time.time()
    data = camera.capture(my_stream, 'bgr', use_video_port=True)
    print(str(time.time() - start2)+" take a picture")
    start2 = time.time()
    if time.time() - start > 5:
        print("help-"+str(i))
        break
    # my_stream.seek(0)
    # my_stream.truncate()
    # camera.capture(my_stream, 'jpeg')
    # camera.capture('/home/pi/Documents/AI/img/test%s.jpg' % i)
start = time.time()
