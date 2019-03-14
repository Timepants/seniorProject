from AccelInterface import AccelInterface as Accel
from Proximity import ProximityInterface as Proximity
import time
import csv
import datetime

class CarLogger(object):
    def __init__(self):
        self.AC = Accel()
        self.PX = Proximity()
        #set up datafile and data writer
        self.dataFile = open('log/manual-'+str(datetime.datetime.now())+'.csv', mode='w')
        self.dataWriter = csv.writer(self.dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
        #make headers
        self.dataWriter.writerow([
        "datetime.now()"
        ,"getAccelX()"
        ,"getAccelY()"
        ,"getAccelZ()"
        ,"getAccelXScaled()"
        ,"getAccelYScaled()"
        ,"getAccelZScaled()"
        ,"getGyroX()"
        ,"getGyroY()"
        ,"getGyroZ()"
        ,"getGyroXScaled()"
        ,"getGyroYScaled()"
        ,"getGyroZScaled()"
        ,"getXRotation()"
        ,"getYRotation()"
        ,"getForwardProximity()"
        ,"steering_angle"
        ,"throttle"])
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
    def write(self, steering_angle, throttle):
        self.dataWriter.writerow([
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
        ,throttle])
    def writeTraining(self):
        print("not written yet")

# car = CarLogger()
# for i in range (200):
#     car.write(i, i*i)
#     time.sleep(0.1)