from AccelInterface import AccelInterface as Accel
from Proximity import ProximityInterface as Proximity
import time
import csv
import datetime
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock, Queue
import conf
import math

class CarLogger(object):
    def __init__(self, putToLog, header):
        self.AC = Accel()
        self.PX = Proximity()
        self.putToLog = putToLog
        self.oldMagnitude = 0
        #set up datafile and data writer
        if self.putToLog:
            self.dataFile = open('log_'+header+'/-'+str(datetime.datetime.now())+'.csv', mode='w')
            self.dataWriter = csv.writer(self.dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
            #make headers
            self.dataWriter.writerow([
            "time"
            ,"accel_x"
            ,"accel_y"
            ,"accel_z"
            ,"accel_x_scaled"
            ,"accel_y_scaled"
            ,"accel_z_scaled"
            ,"gyro_x"
            ,"gyro_y"
            ,"gyro_z"
            ,"gyro_x_scaled"
            ,"gyro_y_scaled"
            ,"gyro_z_scaled"
            ,"x_rotation"
            ,"y_rotation"
            ,"proximity"
            ,"steering_angle"
            ,"throttle"
            ,"count"])
    def printEm(self, steering_angle, throttle):
        print(
        datetime.datetime.now()
        ,self.AC.getAccelX()
        ,self.AC.getAccelY()
        ,self.AC.getAccelZ()
        ,self.AC.getAccelXScaled()
        ,self.AC.getAccelYScaled()
        ,self.AC.getAccelZScaled()
        ,self.AC.getGyroX()
        ,self.AC.getGyroY()
        ,self.AC.getGyroZ()
        ,self.AC.getGyroXScaled()
        ,self.AC.getGyroYScaled()
        ,self.AC.getGyroZScaled()
        ,self.AC.getXRotation()
        ,self.AC.getYRotation()
        ,self.PX.getForwardProximity()
        ,steering_angle
        ,throttle)

    def getData(self, steering_angle, throttle, count):

        try:
            prox = self.PX.getForwardProximity()
        except:
            print("proximity exception")
            prox = -1
        magnitude = math.sqrt(self.AC.getAccelXScaled()**2+self.AC.getAccelYScaled()**2)

        data = {
            "time":datetime.datetime.now()
            ,"accel_x":self.AC.getAccelX()
            ,"accel_y":self.AC.getAccelY()
            ,"accel_z":self.AC.getAccelZ()
            ,"accel_x_scaled":self.AC.getAccelXScaled()
            ,"accel_y_scaled":self.AC.getAccelYScaled()
            ,"accel_z_scaled":self.AC.getAccelZScaled()
            ,"magnitude":magnitude
            ,"gyro_x":self.AC.getGyroX()
            ,"gyro_y":self.AC.getGyroY()
            ,"gyro_z":self.AC.getGyroZ()
            ,"gyro_x_scaled":self.AC.getGyroXScaled()
            ,"gyro_y_scaled":self.AC.getGyroYScaled()
            ,"gyro_z_scaled":self.AC.getGyroZScaled()
            ,"x_rotation":self.AC.getXRotation()
            ,"y_rotation":self.AC.getYRotation()
            ,"proximity":prox
            ,"steering_angle":steering_angle
            ,"throttle":throttle
            ,"count":count
            ,"stop_proximity": True if conf.proximity_stop >= prox and prox != -1 else False
            ,"stop_accel": True if conf.accel_stop <= self.oldMagnitude - magnitude else False
        }
        self.oldMagnitude = magnitude
        return data

    def write(self, steering_angle, throttle, count):
        data = self.getData(steering_angle, throttle, count)

        if self.putToLog:
            self.dataWriter.writerow([
            str(data["time"])
            ,data["accel_x"]
            ,data["accel_y"]
            ,data["accel_z"]
            ,data["accel_x_scaled"]
            ,data["accel_y_scaled"]
            ,data["accel_z_scaled"]
            ,data["gyro_x"]
            ,data["gyro_y"]
            ,data["gyro_z"]
            ,data["gyro_x_scaled"]
            ,data["gyro_y_scaled"]
            ,data["gyro_z_scaled"]
            ,data["x_rotation"]
            ,data["y_rotation"]
            ,data["proximity"]
            ,data["steering_angle"]
            ,data["throttle"]
            ,data["count"]])
            
        return data

# car = CarLogger()
# for i in range (200):
#     car.write(i, i*i)
#     time.sleep(0.1)