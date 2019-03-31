import time
from MotorInterface import MotorInterface as Motor
from picamera import PiCamera
from tkinter import *
from AccelInterface import AccelInterface as Accel
import csv
import datetime

root = Tk()

#TODO make this use the interface not the controller
MC = Motor()

#set up accelerometer interface
# Ac = Accel()

#set up camera stuff
camera = PiCamera()
camera.resolution = (160, 120)

class thingsINeed():
    #create counter for image number
    counter = 14

    #create camera toggle
    isCamera = False

things = thingsINeed()

#set up datafile and data writer
dataFile = open('manual-'+str(datetime.datetime.now())+'.csv', mode='w')
dataWriter = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
#make headers
dataWriter.writerow([
    "datetime.datetime.now()"
    ,"getAccelX()"
    ,"getAccelY()"
    ,"getAccelZ()"
    ,"getGyroX()"
    ,"getGyroY()"
    ,"getGyroZ()"
    ,"get_x_rotation()"
    ,"get_y_rotation()"
    ,"throttle"
    ,"steering"
    ,"movement"])
def addToCSV(throttle, steering, movement):
    dataWriter = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
    dataWriter.writerow([
       str(datetime.datetime.now())
        ,Ac.getAccelX()
        ,Ac.getAccelY()
        ,Ac.getAccelZ()
        ,Ac.getGyroX()
        ,Ac.getGyroY()
        ,Ac.getGyroZ()
        ,Ac.getXRotation()
        ,Ac.getYRotation()
        ,throttle
        ,steering
        ,movement])
    #take a new picture
    if things.isCamera:
        camera.capture('img/frame_'+ str(things.counter).zfill(6) +'_st_'+ str(steering) +'_th_'+ str(throttle) +'.jpg')
        things.counter += 1

def SEND():
    # addToCSV(MC.getThrottle(), MC.getSteering(), MC.getMovement())
    root.after(500, SEND)

def key(event, e):
    inChar = repr(event.char)
    if 'w' in inChar:
        MC.setThrottle(int(e.get("1.0",'end-1c')))
        # MC.sendCommand(MC.FORWARD)
    if 's' in inChar:
        MC.setThrottle(int(e.get("1.0",'end-1c')))
        # MC.sendCommand(MC.BACKWARD)
    if 'z' in inChar:
        MC.stop()
        # MC.sendCommand(MC.CLEAR_ALL)
    if 'e' in inChar:
        MC.setMovement(0)
        # MC.sendCommand(MC.CLEAR_MOVEMENT)
    if 'q' in inChar:
        MC.setSteering(0)
        # MC.sendCommand(MC.CLEAR_HEADING)
    if 'a' in inChar:
        MC.setSteering(-1)
        # MC.sendCommand(MC.LEFT)
    if 'd' in inChar:
        MC.setSteering(1)
        # MC.sendCommand(MC.RIGHT)
    if '1' in inChar:
        # toggle camera
        things.isCamera = not things.isCamera
    MC.printSerial()



def main():
    print("Connecting to Arduino")

    isMoving = False
    isMovingForward = False
    frame = Text(root, width=10, height=1)
    e = Text(root, width=5, height=1)
    frame.bind("<Key>", lambda event, arg=e: key(event, arg))
    frame.pack()
    e.pack()
    frame.focus_set()
    SEND()
    root.mainloop()

    

if  __name__ =='__main__':
    main()
