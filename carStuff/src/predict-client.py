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


class SteeringServer(object):
    def __init__(self, _sio, image_cb = None):
        self.model = None
        # self.timer = FPSTimer()
        self.sio = _sio
        self.app = Flask(__name__)
        self.throttle_man = throttle_manager.ThrottleManager(idealSpeed = 10.)
        self.image_cb = image_cb
        self.counter = 0
        self.counter2 = 0
        self.start = time.time()
        self.start2 = time.time()
        self.start3 = time.time()
        self.responseTime= 0
        self.lastCounter = 0
        self.my_stream = np.empty((128, 160, 3), dtype=np.uint8)

        self.showTime = True
    def telemetry(self, data):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.start3 = time.time()
        if data:
            if self.showTime:
                print("______________________"+str(self.counter2)+"___________________________"+str(self.lastCounter))
                self.responseTime =time.time() - self.start
                
                print(str(self.responseTime)+"   - response time")
                
                self.start = time.time()
                self.counter2 += 1
            # The current steering angle of the car
            steering_angle = float(data["steering_angle"])
            # The current throttle of the car
            throttle = float(data["throttle"])
            # The current speed of the car
            speed = float(data["speed"])
            # The current image from the center camera of the car
            imgString = data["image"]
            # print(imgString)
            # image = Image.open(BytesIO(imgString))

            # image_array = np.asarray(image)
            image_array = np.load(BytesIO(imgString))['frame']

            # if self.showTime:
                # print(str(time.time() - self.start)+"   - loading data")
                # self.start = time.time()

            # if self.image_cb is not None:
            #     self.image_cb(image_array, steering_angle)
            image_array = image_array[:120, :160, :]

            with graph.as_default():
                
                outputs = self.model.predict(image_array[None, :, :, :])
                # outputs = self.model.predict(image_array[:, :, :])

            # if self.showTime:
                # print(str(time.time() - self.start)+"   - NN processing")
                # self.start = time.time()
            #steering
            steering_angle = outputs[0][0]

            #do we get throttle from our network?
            if conf.num_outputs == 2 and len(outputs[0]) == 2:
                throttle = outputs[0][1]
            else:
                #set throttle value here
                throttle, brake = self.throttle_man.get_throttle_brake(speed, steering_angle)

            print(steering_angle, throttle)
            self.send_control(steering_angle, throttle)
            
            if self.showTime:
                # print(str(time.time() - self.start)+"   - send controll time")
                self.start = time.time()            
            self.counter += 1
            if time.time() - self.start2 > 10:
                self.lastCounter = self.counter
                self.start2 = time.time()
                self.counter = 0
                
        else:
            # NOTE: DON'T EDIT THIS.
            self.sio.emit('manual', data={})

        # self.timer.on_frame()

    def connect(self):
        print("connect ")
        # self.timer.reset()
        self.send_control(0, 0)

    def send_control(self, steering_angle, throttle):
        setupTime =(time.time() - self.start3)
        # waitTime = 0.004
        # print(setupTime)
        # # if self.responseTime < 0.15:
        # if setupTime < waitTime: 
        #     time.sleep(waitTime - setupTime)
        # if self.counter2 % 160 == 0:
        #     print("butts")
        #     print("butts")
        #     print("butts")
        #     print("butts")
        #     print("butts")
        #     print("butts")
        #     print("butts")
        #     print("butts")
        #     print("butts")

        #     time.sleep(0.01)
        self.sio.emit(
            "steer",
            data={
                'steering_angle': steering_angle.__str__(),
                'throttle': throttle.__str__()
            })

    def go(self, model_fnm, address):
        
        self.model = keras.models.load_model(model_fnm)
        global graph
        graph = tf.get_default_graph() 
        #In this mode, looks like we have to compile it
        #self.model.compile("sgd", "mse")

        
        self.sio.connect(address)
            # eventlet.wsgi.server(eventlet.listen(address), self.app)
        # except KeyboardInterrupt:
        #     #unless some hits Ctrl+C and then we get this interrupt
        #     print('stopping')


def run_steering_server(address, model_fnm, image_cb=None):

    sio = socketio.Client()

    ss = SteeringServer(sio, image_cb=image_cb)

    @sio.on('telemetry')
    def telemetry(data):
        # print(data)
        ss.telemetry(data)

    @sio.on('connect')
    def connect():
        ss.connect()

    ss.go(model_fnm, address)

# ***** main loop *****
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='prediction server')
    parser.add_argument('model', type=str, help='model name')

    args = parser.parse_args()

    model_fnm = args.model
    address = "http://192.168.4.1:9090"
    run_steering_server(address, model_fnm)
    
