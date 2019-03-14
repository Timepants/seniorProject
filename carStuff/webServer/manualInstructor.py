from MotorInterface import MotorInterface as Motor
from xboxController import runControllerLoop
from picamera import PiCamera
from io import BytesIO


class CarControllerManual(object):
    def __init__(self):
        self.MC = Motor()
        
    def useController(self):
        runControllerLoop(self.MC)
    def getImageStream(self):
        my_stream = BytesIO()
        with PiCamera() as camera:
            while True:
                my_stream.seek(0)
                camera.capture(my_stream, 'jpeg', use_video_port=True)
                return my_stream.getvalue()

# car = CarControllerManual()
# car.useController()