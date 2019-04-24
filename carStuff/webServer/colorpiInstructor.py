#!/usr/bin/env python
'''
Predict Server
Create a server to accept image inputs and run them against a trained neural network.
This then sends the steering output back to the client.
Author: Tawn Kramer
'''
from __future__ import print_function
import os
import argparse
import sys
import time
from datetime import datetime
import shutil
import base64

from PIL import Image
from io import BytesIO
from io import StringIO

from MotorInterface import MotorInterface as Motor
import conf
import throttle_manager
from picamera import PiCamera

import csv
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock, Queue
from piLogger import CarLogger
from basicImageAI import getDirectionFromImage

inputQueueCamera = Queue()
inputQueueMotor = Queue()
outputQueueMotor = Queue()
inputQueueLogger = Queue()
continueRunningAI = True

class CarControllerAI(object):
    def __init__(self):
        self.model = None
        self.MC = Motor()
        self.logger = CarLogger(True, "AI")
        self.throttle_man = throttle_manager.ThrottleManager(idealSpeed = 90.)

        # for counting IPS
        self.counter = 0
        self.start2 = time.time()
        self.lastCounter = 0
        #set up camera stuff
        self.lastDir = 0

        self.pulseInterval = .05
        self.my_stream = BytesIO()
        
        #show debug text?
        self.showTime = True

    def telemetry(self, data, lock, outputQueueMotor, camera):
        iterations = 1
        steering_angle = 0
        for i in range(iterations):
            self.start3 = time.time()
            camera.capture(self.my_stream, 'jpeg', use_video_port=True)

            self.my_stream.seek(0)
            im = Image.open(self.my_stream)
            print("cap and pil", time.time()-self.start3)

            self.start3 = time.time()

            steering_angle += getDirectionFromImage(im, self.lastDir)
            self.lastDir = steering_angle
            print("process", time.time()-self.start3)

            self.my_stream.seek(0)
            self.my_stream.truncate()

        steering_angle = steering_angle / iterations

        outputQueueMotor.put({
            "steering_angle":float(steering_angle)
            ,"throttle":float(conf.manual_speed)
        })
        self.send_control(steering_angle, conf.manual_speed)
        # for effciency counting
        self.counter += 1
        if time.time() - self.start2 > 10:
            self.lastCounter = self.counter
            self.start2 = time.time()
            self.counter = 0


    def send_control(self, steering_angle, throttle):
        self.MC.setSteering(steering_angle)
        self.MC.setThrottle(throttle)
        time.sleep(self.pulseInterval)
        self.MC.setThrottle(conf.slow_manual_speed)
    

    def telemetryLoop(self, lock, inputQueue, outputQueueMotor):
        time.sleep(5)
        with PiCamera() as camera:
            camera.resolution = (160, 128)
            camera.framerate = 60
            camera.rotation =180
            time.sleep(5)
            while continueRunningAI and inputQueue.get():
                data={
                        'steering_angle': self.MC.getSteering(),
                        'throttle': self.MC.getThrottle(),
                        'speed': self.MC.getThrottle()
                    }
                inputQueue.put(True)
                self.telemetry(data, lock, outputQueueMotor, camera)
            else:
                self.MC.setThrottle(0)
        

    def go(self, lock, inputQueue, outputQueueMotor):
        self.telemetryLoop(lock, inputQueue, outputQueueMotor)


    def informationLog(self, inputQueue, outputQueue, outputQueueMotor):
        lastSteering = -999
        lastThrottle = -999
        while inputQueue.get():
            time.sleep(0.5)
            # print("Logger here")
            motorData = skipInQueue(outputQueueMotor)
            try:
                if bool(motorData):
                    data = self.logger.write(motorData["steering_angle"], motorData["throttle"], self.counter)
                    lastSteering = motorData["steering_angle"]
                    lastThrottle = motorData["throttle"]
                else:
                    data = self.logger.write(lastSteering, lastThrottle, self.counter)
            except:
                print("An exception occurred")
            # print(data)
            outputQueue.put(data)
            inputQueue.put(True)
            if(data["stop_proximity"] or data["stop_accel"]):
                stop()
        else:
            skipInQueue(outputQueue)
            skipInQueue(outputQueueMotor)
            
def stopQueue(queue):
    while not queue.empty():
        queue.get() 
    for i in range(20):
        queue.put(False)

def startQueue(queue):
    while not queue.empty():
        queue.get() 
    queue.put(True)

def stop():
    stopQueue(inputQueueCamera)
    stopQueue(inputQueueMotor)
    stopQueue(inputQueueLogger)
    skipInQueue(outputQueueMotor)

def skipInQueue(queue):
    data = dict()
    while not queue.empty():
        data = queue.get()
    return data

def run_color_AI(outputQueue):
    pool = ThreadPool(processes=2)
    lock = Lock()   

    ss = CarControllerAI()
    startQueue(inputQueueCamera)
    startQueue(inputQueueMotor)
    startQueue(inputQueueLogger)
    skipInQueue(outputQueueMotor)
    pool.apply_async(ss.go, (lock, inputQueueMotor, outputQueueMotor))
    
    time.sleep(0.01)

    result = pool.apply_async(ss.informationLog, (inputQueueLogger, outputQueue, outputQueueMotor)) 

# ***** main loop *****
if __name__ == "__main__":
    outputQueue = Queue()

    run_color_AI(outputQueue)
    try:
        while True:
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(outputQueue.get())
                
    except KeyboardInterrupt:
            print ('Interrupted - closing')
            stop()
            time.sleep(0.5)
            sys.exit(0)

