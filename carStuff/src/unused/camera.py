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
import os


camera = PiCamera()
camera.resolution = (160, 128)
# camera.shutter_speed = 800

camera.framerate = 60

# camera.video_stabilization = True
my_stream2 = BytesIO()
my_stream = np.empty((128, 160, 3), dtype=np.uint8)
time.sleep(1)
start = time.time()

accumTotal = 0

for q in range(1):
    for i in range(1000):
        # sleep(0.5)
        

        start2 = time.time()
        camera.capture(my_stream, 'bgr', use_video_port=True)

        f = BytesIO()
        np.savez_compressed(f,frame=my_stream)
        f.seek(0)
        out = f.read()
        os.system('cls' if os.name == 'nt' else 'clear')
        accumTotal +=time.time() - start2
        print(str(time.time() - start2)+" take a picture bgr")
        start2 = time.time()
        time.sleep(0.008)

        start2 = time.time()
        camera.capture(my_stream2, 'jpeg', use_video_port=True)
        accumTotal -=time.time() - start2
        print(str(time.time() - start2)+" take a picture jpeg")
        start2 = time.time()

        print(str(accumTotal))

        # if time.time() - start > 10:
        #     print("help-"+str(i))
        #     break
        # my_stream.seek(0)
        # my_stream.truncate()
        # camera.capture(my_stream, 'jpeg')
        # camera.capture('/home/pi/Documents/AI/img/test%s.jpg' % i)
    start = time.time()
