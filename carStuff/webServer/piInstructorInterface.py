#!/usr/bin/env python
import os
import sys
import time
import csv
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock, Queue
import random

class CarControllerAI(object):
    def __init__(self):
        self.lastCounter = 0


    def telemetry(self, data, outputQueue, lock):
        if data:
            # print(steering_angle, throttle)
            print("its me, the pi instructor: ", self.lastCounter)
            outputQueue.put({"steering":random.randint(-1,1)
                            , "throttle":random.randint(85,100)
                            ,"accel":random.randrange(0,4)})
            self.lastCounter += 1


    def telemetryLoop(self, outputQueue, lock, inputQueue):
        while inputQueue.get(): 
            print("Telem")
            time.sleep(0.1)  
            data={
                    'steering_angle': 0,
                    'throttle': 90,
                    'speed': 90
                }
            # self.getCameraData()
            inputQueue.put(True)
            self.telemetry(data, outputQueue, lock)   

    def go(self, model_fnm, outputQueue, lock, inputQueue):
        print("go")
        self.telemetryLoop(outputQueue, lock, inputQueue)

inputQueue = Queue()


def stop():
    print("trying to stop")
    while not inputQueue.empty():
        inputQueue.get() 
    inputQueue.put(False)


def run_steering_server(model_fnm, outputQueue):
    print("run")
    pool = ThreadPool(processes=1)

    lock = Lock()   
    print("pool and lock")
    ss = CarControllerAI()
    print("ss")
    time.sleep(0.01)

    while not inputQueue.empty():
        inputQueue.get() 

    inputQueue.put(True)
    print("inputQ")
    # ss.go(model_fnm ,outputQueue, lock, inputQueue)

    async_result = pool.apply_async(ss.go, (model_fnm ,outputQueue, lock, inputQueue)) # tuple of args for foo
    # return_val = async_result.get()  # get the return value from your function.
    print("gone")
    # print(return_val)
    # ss.go(model_fnm)

# ***** main loop *****
if __name__ == "__main__":

    outputQueue = Queue()


    run_steering_server("boots", outputQueue)
    try:
        while True:
            time.sleep(0.1)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(outputQueue.get())

                
    except KeyboardInterrupt:
            print ('Interrupted - closing')
            continueRunningAI = False
            time.sleep(0.5)
            sys.exit(0)

    
