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

import numpy as np
import socketio
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO
from io import StringIO
import keras
import tensorflow as tf

from MotorInterface import MotorInterface as Motor
import conf
import throttle_manager
from picamera import PiCamera

import csv
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock, Queue
from piLogger import CarLogger

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


        self.my_stream = np.empty((128, 160, 3), dtype=np.uint8)
        
        #show debug text?
        self.showTime = True

    def getCameraData(self, lock, inputQueue):
        global image_array
        with PiCamera() as camera:
            camera.resolution = (160, 128)
            camera.framerate = 60
            time.sleep(5)
            # global continueRunningAI
            while continueRunningAI and inputQueue.get():
            
                time.sleep(0.05)
                # print("its me the camera")

                camera.capture(self.my_stream, 'bgr', use_video_port=True)
                lock.acquire()
                image_array = self.my_stream[:120, :160, :]
                lock.release()

                inputQueue.put(True)


            return image_array

    def telemetry(self, data, lock, outputQueueMotor):
        if data:
            # The current steering angle of the car
            steering_angle = float(data["steering_angle"])
            # The current throttle of the car
            throttle = float(data["throttle"])
            # The current speed of the car
            speed = float(data["speed"])
            lock.acquire()
            inImage = image_array
            lock.release()
            # get information from model
            outputs = self.model.predict(inImage[None, :, :, :])

            steering_angle = outputs[0][0]

            #do we get throttle from our network?
            if conf.num_outputs == 2 and len(outputs[0]) == 2:
                throttle = outputs[0][1]
            else:
                #set throttle value here
                #throttle, brake = self.throttle_man.get_throttle_brake(speed, steering_angle)
                throttle = conf.manual_speed

            # print(steering_angle, throttle)
            outputQueueMotor.put({
                "steering_angle":float(steering_angle)
                ,"throttle":float(throttle)
            })
            self.send_control(steering_angle, throttle)
            
            # for effciency counting
            self.counter += 1
            if time.time() - self.start2 > 10:
                self.lastCounter = self.counter
                self.start2 = time.time()
                self.counter = 0


    def send_control(self, steering_angle, throttle):
        self.MC.setSteering(steering_angle)
        self.MC.setThrottle(throttle)
    

    def telemetryLoop(self, lock, inputQueue, outputQueueMotor):
        while continueRunningAI and inputQueue.get():
            data={
                    'steering_angle': self.MC.getSteering(),
                    'throttle': self.MC.getThrottle(),
                    'speed': self.MC.getThrottle()
                }
            inputQueue.put(True)
            self.telemetry(data, lock, outputQueueMotor)   

    def go(self, model_fnm, lock, inputQueue, outputQueueMotor):
        
        self.model = keras.models.load_model(model_fnm)
        global continueRunningAI
        self.telemetryLoop(lock, inputQueue, outputQueueMotor)
        keras.backend.clear_session()

    def informationLog(self, inputQueue, outputQueue, outputQueueMotor):
        while inputQueue.get():
            time.sleep(0.05)
            motorData = skipInQueue(outputQueueMotor)
            try:
                if bool(motorData):
                    data = self.logger.write(motorData["steering_angle"], motorData["throttle"], self.counter)
                else:
                    data = self.logger.write(0, 0, self.counter)
            except:
                print("An exception occurred")
            outputQueue.put(data)
            inputQueue.put(True)

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

def skipInQueue(queue):
    data = dict()
    while not queue.empty():
        data = queue.get()
    return data

def run_steering_server(model_fnm, outputQueue):


    pool = ThreadPool(processes=3)
    lock = Lock()   

    ss = CarControllerAI()
    startQueue(inputQueueCamera)
    startQueue(inputQueueMotor)
    startQueue(inputQueueLogger)

    # ss.informationLog(inputQueueLogger, outputQueue)

    cameraRelsult = pool.apply_async(ss.getCameraData, (lock, inputQueueCamera)) 
    time.sleep(0.01)

    async_result = pool.apply_async(ss.go, (model_fnm, lock, inputQueueMotor, outputQueueMotor))
    
    time.sleep(0.01)

    result = pool.apply_async(ss.informationLog, (inputQueueLogger, outputQueue, outputQueueMotor)) 

    # ss.go(model_fnm, lock, inputQueueMotor, outputQueueMotor)
# ***** main loop *****
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='prediction server')
    parser.add_argument('model', type=str, help='model name')

    args = parser.parse_args()
    outputQueue = Queue()

    model_fnm = args.model
    run_steering_server(model_fnm, outputQueue)
    try:
        while True:
            time.sleep(0.1)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(outputQueue.get())

                
    except KeyboardInterrupt:
            print ('Interrupted - closing')
            stop()
            time.sleep(0.5)
            sys.exit(0)

