import socketio
from picamera import PiCamera
from time import sleep
import base64
from io import BytesIO
from MotorInterface import MotorInterface as Motor

MC = Motor()
sio = socketio.Client()


camera = PiCamera()
camera.resolution = (160, 120)
sleep(2)
my_stream = BytesIO()
@sio.on('connect')
def on_connect():
    print('connection established')
    
    # for i in range(20):
    # camera.capture(my_stream, 'jpeg')
    # print("test")
    # sleep(0.2)
    # data =	{
    #     "steering_angle": 0,
    #     "throttle": 0.5,
    #     "speed": 0.5,
    #     "image": my_stream.getvalue()
    # }
    # sio.emit('telemetry', data)

@sio.on('steer')
def on_message(data):
    print(my_stream.getbuffer().nbytes)
    my_stream.seek(0)
    print('message s received with ', data)
    MC.setSteering(float(data['steering_angle']))
    print(float(data['throttle']))
    MC.setThrottle(float(data['throttle']))
    camera.capture(my_stream, 'jpeg')
    print("test")
    sleep(0.2)
    data =	{
        "steering_angle": 0,
        "throttle": 0.5,
        "speed": 0.5,
        "image": my_stream.getvalue()
    }
    sio.emit('telemetry', data)

@sio.on('disconnect')
def on_disconnect():
    MC.stop()
    print('disconnected from server')

sio.connect('http://192.168.4.17:9090')
sio.wait()

