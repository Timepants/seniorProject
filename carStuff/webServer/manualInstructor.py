from MotorInterface import MotorInterface as Motor
from xboxController import runControllerLoop
from picamera import PiCamera
from io import BytesIO
from piLogger import CarLogger

from multiprocessing.pool import ThreadPool
from multiprocessing import Lock, Queue
import time
import sys
import os

class CarControllerManual(object):
    def __init__(self):
        self.MC = Motor()
        self.imgCount = 0
        self.logger = CarLogger(True, "manual")

    def useController(self, inputQueue):
        print("wo")
        runControllerLoop(self.MC, inputQueue)
    def logPhotos(self, inputQueue, inputQueueControllerButton):
        files = os.listdir("training_img/")
        # find number of last file
        for f in files:
            p = f.split("_")
            if int(p[1]) >= self.imgCount:
                self.imgCount = int(p[1])+1
                print(int(p[1]))
        with PiCamera() as camera:
            camera.rotation = 180
            camera.resolution = (160, 120)
            camera.framerate = 60
            while inputQueue.get(): 
                # print(inputQueueControllerButton.empty())              
                if not inputQueueControllerButton.empty() and inputQueueControllerButton.get():
                    imgLocation = "training_img/frame_"+str(self.imgCount).zfill(6)+"_st_"+str(self.MC.getSteering())+"_th_"+str(self.MC.getThrottle())+".jpg"
                    # print(imgLocation)
                    camera.capture(imgLocation, 'jpeg', use_video_port=True)
                    inputQueueControllerButton.put(True)
                    self.imgCount += 1
                else:
                    time.sleep(0.1)
                    inputQueueControllerButton.put(False)
                inputQueue.put(True)

    def informationLog(self, inputQueue, outputQueue):
        while inputQueue.get():
            data = self.logger.write(self.MC.getSteering(), self.MC.getThrottle(), self.imgCount)
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

def stopMan():
    stopQueue(inputQueueController)
    stopQueue(inputQueueImage)
    stopQueue(inputQueueLogger)

def startQueue(queue):
    while not queue.empty():
        queue.get() 
    queue.put(True)

pool = ThreadPool(processes=3)

def runInstructor(outputQueue):
    
    lock = Lock()   

    control = CarControllerManual()

    stopQueue(inputQueueController)
    startQueue(inputQueueLogger)
    startQueue(inputQueueImage)

    print("whats the deal")

    # control.informationLog(inputQueueLogger, outputQueue)

    pool.apply_async(control.useController, (inputQueueController, )) 
    time.sleep(0.01)

    pool.apply_async(control.informationLog, (inputQueueLogger, outputQueue)) 

    time.sleep(0.01)

    pool.apply_async(control.logPhotos, (inputQueueImage, inputQueueController)) 
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
            # print(skipInQueue(outputQueue))

                
    except KeyboardInterrupt:
            # print ('Interrupted - closing')
            stopMan()
            time.sleep(0.5)
            sys.exit(0)

    # car = CarControllerManual()
    # car.useController()