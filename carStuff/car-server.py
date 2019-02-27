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
import keras

from picamera import PiCamera
import time
from MotorInterface import MotorInterface as Motor
from AccelInterface import AccelInterface as Accel
import csv
import datetime

class SteeringServer(object):
    def __init__(self, _sio):

        #get motor ready
        self.MC = Motor()
        self.sio = _sio

        #set up camera stuff
        self.camera = PiCamera()
        self.camera.resolution = (160, 120)
        time.sleep(2)
        self.my_stream = BytesIO()

    def steer(self, sid, data):
        #TODO add emergency stop
        #reset photo stream
        self.my_stream.seek(0)
    
        #get incoming data and set
        # print('message s received with ', data)
        self.MC.setSteering(float(data['steering_angle']))
        # MC.setThrottle(float(data['throttle']), 1)
        self.MC.setThrottle(90)

        if float(data['steering_angle'])  > 1.5:
            print ("right")
        elif float(data['steering_angle'])  < -1.5:
            print("left")
        else:
            print("straight")
        #TODO add to log file
        # addToCSV(MC.getThrottle(), MC.getSteering(), MC.getMovement())
        # print(things.counter)
        # print(MC.printSerial())
        #take a new picture
        self.camera.capture(self.my_stream, 'jpeg', use_video_port=True)
        # time.sleep(interval)
        #send response data
        #TODO this should not have to return speed
        data =	{
            "steering_angle": self.MC.getSteering(),
            "throttle": self.MC.getThrottle(),
            "speed": self.MC.getThrottle(),
            "image": self.my_stream.getvalue()
        }
        self.sio.emit('telemetry', data)

    def connect(self, sid, environ):
        print("connect ", sid)


    def go(self, address):
        # wrap Flask application with engineio's middleware
        self.app = socketio.Middleware(self.sio, self.app)

        # deploy as an eventlet WSGI server
        try:
            eventlet.wsgi.server(eventlet.listen(address), self.app)
        except KeyboardInterrupt:
            #unless some hits Ctrl+C and then we get this interrupt
            print('stopping')


def run_steering_server(address):

    sio = socketio.Server()

    ss = SteeringServer(sio)

    @sio.on('steer')
    def steer(sid, data):
        # print(data)
        ss.steer(sid, data)

    @sio.on('connect')
    def connect(sid, environ):
        ss.connect(sid, environ)

    ss.go(address)

# ***** main loop *****
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='prediction server')
    # parser.add_argument('model', type=str, help='model name')
    # parser.add_argument(
    #       'image_folder',
    #       type=str,
    #       nargs='?',
    #       default=None,
    #       help='Path to image folder. This is where the images from the run will be saved.'
    #   )

    # args = parser.parse_args()

    # if args.image_folder is not None:
    #     print("Creating image folder at {}".format(args.image_folder))
    #     if not os.path.exists(args.image_folder):
    #         os.makedirs(args.image_folder)
    #     else:
    #         shutil.rmtree(args.image_folder)
    #         os.makedirs(args.image_folder)
    #     print("RECORDING THIS RUN ...")

    # model_fnm = args.model
    address = ('', 9090)
    run_steering_server(address)
    
