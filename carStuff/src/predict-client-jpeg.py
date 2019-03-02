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
    def __init__(self, _sio, image_folder = None, image_cb = None):
        self.model = None
        # self.timer = FPSTimer()
        self.sio = _sio
        self.app = Flask(__name__)
        self.throttle_man = throttle_manager.ThrottleManager(idealSpeed = 10.)
        self.image_cb = image_cb
        self.image_folder = image_folder
        self.counter = 0
        self.start = time.time()

    def telemetry(self, data):
        if data:
            # The current steering angle of the car
            steering_angle = float(data["steering_angle"])
            # The current throttle of the car
            throttle = float(data["throttle"])
            # The current speed of the car
            speed = float(data["speed"])
            # The current image from the center camera of the car
            imgString = data["image"]
            # print(imgString)
            image = Image.open(BytesIO(imgString))

            image_array = np.asarray(image)
            # image_array = np.load(BytesIO(imgString))['frame']
            # if self.image_cb is not None:
            #     self.image_cb(image_array, steering_angle)
            
            with graph.as_default():
                outputs = self.model.predict(image_array[None, :, :, :])

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
            
            self.counter += 1
            if time.time() - self.start > 10:
                print("Time----------------------------------------"+str(self.counter))
                self.start = time.time()
                self.counter = 0

            # save frame
            if self.image_folder is not None:
                timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
                image_filename = os.path.join(self.image_folder, timestamp)
                image.save('{}.jpg'.format(image_filename))
        else:
            # NOTE: DON'T EDIT THIS.
            self.sio.emit('manual', data={})

        # self.timer.on_frame()

    def connect(self):
        print("connect ")
        # self.timer.reset()
        self.send_control(0, 0)

    def send_control(self, steering_angle, throttle):
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


def run_steering_server(address, model_fnm, image_folder=None, image_cb=None):

    sio = socketio.Client()

    ss = SteeringServer(sio, image_cb=image_cb, image_folder=image_folder)

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
    parser.add_argument(
          'image_folder',
          type=str,
          nargs='?',
          default=None,
          help='Path to image folder. This is where the images from the run will be saved.'
      )

    args = parser.parse_args()

    if args.image_folder is not None:
        print("Creating image folder at {}".format(args.image_folder))
        if not os.path.exists(args.image_folder):
            os.makedirs(args.image_folder)
        else:
            shutil.rmtree(args.image_folder)
            os.makedirs(args.image_folder)
        print("RECORDING THIS RUN ...")

    model_fnm = args.model
    address = "http://192.168.4.1:9090"
    run_steering_server(address, model_fnm, image_folder=args.image_folder)
    
