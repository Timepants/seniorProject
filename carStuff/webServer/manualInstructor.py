from MotorInterface import MotorInterface as Motor
from xboxController import runControllerLoop
from picamera import PiCamera
from io import BytesIO
from piLogger import CarLogger

from multiprocessing.pool import ThreadPool
from multiprocessing import Lock, Queue
import time
import sys

class CarControllerManual(object):
    def __init__(self):
        self.MC = Motor()
        self.imgCount = 0
        self.logger = CarLogger(True, "manual")

    def useController(self, inputQueue):
        print("wo")
        runControllerLoop(self.MC)
    def logPhotos(self, inputQueue):
        print("method")
        with PiCamera() as camera:
            camera.resolution = (160, 120)
            camera.framerate = 60
            while inputQueue.get():
                imgLocation = "training_img/frame_"+str(self.imgCount).zfill(6)+"_st_"+str(self.MC.getSteering())+"_th_"+str(self.MC.getThrottle())+".jpg"
                # print(imgLocation)
                camera.capture(imgLocation, 'jpeg', use_video_port=True)

                inputQueue.put(True)
                self.imgCount += 1

    def informationLog(self, inputQueue, outputQueue):
        print()
        while inputQueue.get():
            data = self.logger.write(self.MC.getSteering(), self.MC.getThrottle(), self.imgCount)
            # print("boi")
            outputQueue.put(data)
            inputQueue.put(True)

inputQueueController = Queue()
inputQueueImage = Queue()
inputQueueLogger = Queue()

def stopQueue(queue):
    while not queue.empty():
        queue.get() 
    for i in range(20):
        queue.put(False)

def stop():
    stopQueue(inputQueueController)
    stopQueue(inputQueueImage)
    stopQueue(inputQueueLogger)

def startQueue(queue):
    while not queue.empty():
        queue.get() 
    queue.put(True)

def runInstructor(outputQueue):
    pool = ThreadPool(processes=3)
    lock = Lock()   

    control = CarControllerManual()

    startQueue(inputQueueController)
    startQueue(inputQueueImage)
    startQueue(inputQueueLogger)

    print("whats the deal")

    # control.informationLog(inputQueueLogger, outputQueue)

    pool.apply_async(control.useController, (inputQueueController, )) 
    time.sleep(0.01)

    pool.apply_async(control.logPhotos, (inputQueueImage, )) 

    time.sleep(0.01)

    pool.apply_async(control.informationLog, (inputQueueLogger, outputQueue)) 

    # control.logPhotos(inputQueueController)

def skipInQueue(queue):
    data = dict()
    while not queue.empty():
        data = queue.get()
    return data

if __name__ == "__main__":
    outputQueue = Queue()

    runInstructor(outputQueue)

    try:
        while True:
            time.sleep(1)
            # os.system('cls' if os.name == 'nt' else 'clear')
            print(skipInQueue(outputQueue))

                
    except KeyboardInterrupt:
            print ('Interrupted - closing')
            stop()
            time.sleep(0.5)
            sys.exit(0)

    # car = CarControllerManual()
    # car.useController()