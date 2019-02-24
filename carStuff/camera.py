from picamera import PiCamera
from time import sleep
from io import BytesIO
import time
camera = PiCamera()
camera.resolution = (160, 120)
camera.shutter_speed = 800
# camera.framerate = 900
camera.video_stabilization = True
my_stream = BytesIO()
sleep(2)
start = time.time()
for i in range(5000):
    # sleep(0.5)
    print("help-"+str(i))
    data =	{
        "steering_angle": 0,
        "throttle": 0.5,
        "speed": 0.5,
        "image": camera.capture(my_stream, 'jpeg', use_video_port=True)
    }
    if time.time() - start > 5:
        break
    my_stream.seek(0)
    my_stream.truncate()
    # camera.capture(my_stream, 'jpeg')
    # camera.capture('/home/pi/Documents/AI/img/test%s.jpg' % i)
# start = time.time()
# my_stream.seek(0)
# counter = 0
# for foo in camera.capture_continuous(my_stream, 'jpeg'):
#     # Write the length of the capture to the stream and flush to
#     # ensure it actually gets sent
#     print("help2-" + str(counter))
#     counter += 1
#     data =	{
#         "steering_angle": 0,
#         "throttle": 90,
#         "speed": 90,
#         "image": my_stream.getvalue()
#     }
#     # sio.emit('telemetry', data)
#     # If we've been capturing for more than 30 seconds, quit
#     if time.time() - start > 10:
#         break
#     # Reset the stream for the next capture
#     my_stream.seek(0)
#     my_stream.truncate()

# my_stream.seek(0)
# camera.resolution = (160, 128)
# for foo in camera.capture_continuous(my_stream, 'bgr'):
#     # Write the length of the capture to the stream and flush to
#     # ensure it actually gets sent
#     print("help3")
#     data =	{
#         "steering_angle": 0,
#         "throttle": 90,
#         "speed": 90,
#         "image": my_stream.getvalue()
#     }
#     # sio.emit('telemetry', data)
#     # If we've been capturing for more than 30 seconds, quit
#     if time.time() - start > 10:
#         break
#     # Reset the stream for the next capture
#     my_stream.seek(0)
#     my_stream.truncate()
#capture to a stream
#camera.capture(my_stream, 'jpeg')