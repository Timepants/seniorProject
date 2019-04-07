import socketio
from picamera import PiCamera
import time
import base64
from io import BytesIO
from MotorInterface import MotorInterface as Motor
from AccelInterface import AccelInterface as Accel
import csv
import datetime

#interval of transmission in seconds
interval = 0.02

#get motor ready
MC = Motor()

#get client ready
sio = socketio.Client()

#set up camera stuff
camera = PiCamera()
camera.resolution = (160, 128)
time.sleep(2)
my_stream = BytesIO()
# camera.capture(my_stream, 'jpeg')

class thingsINeed():
    #create counter for image number
    counter =0 

things = thingsINeed()

@sio.on('connect')
def on_connect():
    counter = 0
    print('connection established')
    start = time.time()
    my_stream.seek(0)
    for foo in camera.capture_continuous(my_stream, 'bgr'):
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        data =	{
            "steering_angle": 0,
            "throttle": 90,
            "speed": 90,
            "image": my_stream.getvalue()
        }
        sio.emit('telemetry', data)
        # If we've been capturing for more than 30 seconds, quit
        if time.time() - start > 30:
            break
        # Reset the stream for the next capture
        my_stream.seek(0)
        my_stream.truncate()
    # Write a length of zero to the stream to signal we're done
    #add to log file
    # addToCSV(MC.getThrottle(), MC.getSteering(), MC.getMovement())
    # print(things.counter)
    # print(MC.printSerial())
    things.counter += 1
    #take a new picture
    # camera.capture(my_stream, 'jpeg')
    # time.sleep(interval)
    #send response data
    #TODO this should not have to return speed



@sio.on('disconnect')
def on_disconnect():
    MC.stop()
    print('disconnected from server')

sio.connect('http://192.168.4.18:9090')
sio.wait()

