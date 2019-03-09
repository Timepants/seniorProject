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

import conf
import throttle_manager
from picamera import PiCamera
from MotorInterface import MotorInterface as Motor
from AccelInterface import AccelInterface as Accel
import csv
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock, Queue

continueRunningAI = True

class CarControllerAI(object):
    def __init__(self):
        self.model = None
        self.MC = Motor()
        # self.AC = Accel()
        self.throttle_man = throttle_manager.ThrottleManager(idealSpeed = 10.)

        # for counting IPS
        self.counter = 0
        self.start2 = time.time()
        self.lastCounter = 0
        #set up camera stuff
        self.camera = PiCamera()
        self.camera.resolution = (160, 128)
        self.camera.framerate = 60
        self.my_stream = np.empty((128, 160, 3), dtype=np.uint8)
        
        #show debug text?
        self.showTime = True

    def getCameraData(self, lock):
            
            global image_array
            # global continueRunningAI
            while continueRunningAI:
                time.sleep(0.005)
                # print("its me the camera")

                self.camera.capture(self.my_stream, 'bgr', use_video_port=True)
                lock.acquire()
                image_array = self.my_stream[:120, :160, :]
                lock.release()

            return image_array

    def telemetry(self, data, outputQueue, lock):
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
                throttle, brake = self.throttle_man.get_throttle_brake(speed, steering_angle)

            # print(steering_angle, throttle)
            outputQueue.put([self.lastCounter, steering_angle,throttle])
            self.send_control(steering_angle, throttle)
            
            # for effciency counting
            self.counter += 1
            if time.time() - self.start2 > 10:
                self.lastCounter = self.counter
                self.start2 = time.time()
                self.counter = 0


    def send_control(self, steering_angle, throttle):

        # print(self.AC.getAccelX()
        # ,self.AC.getAccelY()
        # ,self.AC.getAccelZ()
        # ,self.AC.getGyroX()
        # ,self.AC.getGyroY()
        # ,self.AC.getGyroZ()
        # ,self.AC.getXRotation()
        # ,self.AC.getYRotation())
        self.MC.setSteering(steering_angle)
        self.MC.setThrottle(throttle)

    

    def telemetryLoop(self, outputQueue, lock):
        while continueRunningAI:    
            data={
                    'steering_angle': self.MC.getSteering(),
                    'throttle': self.MC.getThrottle(),
                    'speed': self.MC.getThrottle()
                }
            # self.getCameraData()
            self.telemetry(data, outputQueue, lock)   

    def go(self, model_fnm, outputQueue, lock):
        
        self.model = keras.models.load_model(model_fnm)

        global continueRunningAI

        self.telemetryLoop(outputQueue, lock)




def run_steering_server(model_fnm, outputQueue):
    pool = ThreadPool(processes=2)

    lock = Lock()   

    ss = CarControllerAI()
    


    cameraRelsult = pool.apply_async(ss.getCameraData, (lock,)) # tuple of args for foo

    time.sleep(0.01)

    async_result = pool.apply_async(ss.go, (model_fnm,outputQueue, lock)) # tuple of args for foo

    # return_val = async_result.get()  # get the return value from your function.

    # print(return_val)
    # ss.go(model_fnm)

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
            continueRunningAI = False
            time.sleep(0.5)
            sys.exit(0)

    
