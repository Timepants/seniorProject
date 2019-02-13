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
camera.resolution = (160, 120)
time.sleep(2)
my_stream = BytesIO()

#set up accelerometer interface
Ac = Accel()

#set up datafile and data writer
dataFile = open('log-'+str(datetime.datetime.now())+'.csv', mode='w')
dataWriter = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
#make headers
dataWriter.writerow([
    "datetime.datetime.now()"
    ,"getAccelX()"
    ,"getAccelY()"
    ,"getAccelZ()"
    ,"getGyroX()"
    ,"getGyroY()"
    ,"getGyroZ()"
    ,"get_x_rotation()"
    ,"get_y_rotation()"
    ,"throttle"
    ,"steering"
    ,"movement"])
def addToCSV(throttle, steering, movement):
    dataWriter = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
    dataWriter.writerow([
       str(datetime.datetime.now())
        ,Ac.getAccelX()
        ,Ac.getAccelY()
        ,Ac.getAccelZ()
        ,Ac.getGyroX()
        ,Ac.getGyroY()
        ,Ac.getGyroZ()
        ,Ac.getXRotation()
        ,Ac.getYRotation()
        ,throttle
        ,steering
        ,movement])

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on('steer')
def on_message(data):
    #TODO add emergency stop
    #reset photo stream
    my_stream.seek(0)
   
    #get incoming data and set
    print('message s received with ', data)
    MC.setSteering(float(data['steering_angle']))
    MC.setThrottle(float(data['throttle']))
    
    #add to log file
    addToCSV(MC.getThrottle(), MC.getSteering(), MC.getMovement())

    #take a new picture
    camera.capture(my_stream, 'jpeg')
    time.sleep(interval)
    #send response data
    #TODO this should not have to return speed
    data =	{
        "steering_angle": MC.getSteering(),
        "throttle": MC.getThrottle(),
        "speed": MC.getThrottle(),
        "image": my_stream.getvalue()
    }
    sio.emit('telemetry', data)

@sio.on('disconnect')
def on_disconnect():
    MC.stop()
    print('disconnected from server')

sio.connect('http://192.168.4.17:9090')
sio.wait()

