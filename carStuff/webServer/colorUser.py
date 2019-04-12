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
from PIL import Image
from flask import Flask
from io import BytesIO
from io import StringIO

import conf
import throttle_manager
from picamera import PiCamera
from MotorInterface import MotorInterface as Motor
from AccelInterface import AccelInterface as Accel
import csv

from basicImageAI import getDirectionFromImage

class CarControllerAI(object):
    def __init__(self, image_cb = None):
        self.model = None
        self.MC = Motor()
        # self.AC = Accel()
        self.pulseInterval = .05
        self.throttle_man = throttle_manager.ThrottleManager(idealSpeed = 10.)
        self.image_cb = image_cb
        self.counter = 0
        self.counter2 = 0
        self.start = time.time()
        self.start2 = time.time()
        self.start3 = time.time()
        self.responseTime= 0
        self.lastCounter = 0
        #set up camera stuff
        self.camera = PiCamera()
        self.camera.resolution = (160, 128)
        self.camera.framerate = 60
        self.my_stream = BytesIO()
        self.showTime = True
        time.sleep(1.5)

        

    def telemetry(self, data):
        
        
        if data:
            if self.showTime:
                # os.system('cls' if os.name == 'nt' else 'clear')
                print("______________________"+str(self.counter2)+"___________________________"+str(self.lastCounter))
                self.responseTime =time.time() - self.start
                
                print(str(self.responseTime)+"   - response time")
                
                self.start = time.time()
                self.counter2 += 1

            # time.sleep(1)
            iterations = 1
            steering_angle = 0
            for i in range(iterations):
                self.start3 = time.time()
                self.camera.capture(self.my_stream, 'jpeg', use_video_port=True)

                self.my_stream.seek(0)
                im = Image.open(self.my_stream)
                print("cap and pil", time.time()-self.start3)

                self.start3 = time.time()

                steering_angle += getDirectionFromImage(im)
                print("process", time.time()-self.start3)

                self.my_stream.seek(0)
                self.my_stream.truncate()

            steering_angle = steering_angle / iterations

            self.send_control(steering_angle, conf.manual_speed)
            
            # if self.showTime:
            #     # print(str(time.time() - self.start)+"   - send controll time")
            #     self.start = time.time()            
            self.counter += 1
            if time.time() - self.start2 > 10:
                self.lastCounter = self.counter
                self.start2 = time.time()
                self.counter = 0
                
        # self.timer.on_frame()

    def send_control(self, steering_angle, throttle):
        print("send",steering_angle,throttle)
        setupTime =(time.time() - self.start3)
        self.MC.setSteering(steering_angle)
        self.MC.setThrottle(throttle)
        time.sleep(self.pulseInterval)
        self.MC.setThrottle(60)

    def go(self):

        data={
                'steering_angle': 0,
                'throttle': 90,
                'speed': 90
            }
        for i in range(3000):
            self.telemetry(data)   

        # self.sio.connect(address)
            # eventlet.wsgi.server(eventlet.listen(address), self.app)
        # except KeyboardInterrupt:
        #     #unless some hits Ctrl+C and then we get this interrupt
        #     print('stopping')


def run_steering_server(image_cb=None):

    ss = CarControllerAI(image_cb=image_cb)

    ss.go()

# ***** main loop *****
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='prediction server')
    # parser.add_argument('model', type=str, help='model name')

    # args = parser.parse_args()

    # model_fnm = args.model
    run_steering_server()
    
