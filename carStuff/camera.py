from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (160, 120)
sleep(2)
for i in range(20):
    sleep(0.5)
    data =	{
        "steering_angle": 0,
        "throttle": 0.5,
        "speed": 0.5,
        "image": camera.capture(my_stream, 'jpeg')
    }
    # camera.capture(my_stream, 'jpeg')
    # camera.capture('/home/pi/Documents/AI/img/test%s.jpg' % i)


#capture to a stream
#camera.capture(my_stream, 'jpeg')