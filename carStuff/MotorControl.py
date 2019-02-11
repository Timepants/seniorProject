import serial
import time

class MotorContol(object):
    FORWARD = 'f'
    BACKWARD = 'b'
    CLEAR_MOVEMENT = 'm'
    LEFT = 'l'
    RIGHT = 'r'
    CLEAR_HEADING = 'h'
    CLEAR_ALL = 's'
    NOT_SET = 'x'

    def __init__(self):
        time.sleep(3)
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.currentMovement = 'x'
        self.currentHeading = 'x'
        self.throttle = 0
    
    def getMovement():
        return self.currentMovement
    
    def getHeading():
        return self.currentHeading

    def getThrottle():
        return self.throttle
    
    def sendCommand(self, command):
        if command == self.FORWARD or command == self.BACKWARD:
            self.currentMovement = command
        elif command == self.LEFT or command == self.RIGHT:
            self.currentHeading = command
        elif command == self.CLEAR_HEADING:
            self.currentHeading = self.NOT_SET
        elif command == self.CLEAR_MOVEMENT:
            self.currentMovement = self.NOT_SET
        else:
            self.currentHeading = self.NOT_SET
            self.currentMovement = self.NOT_SET

        self.currentMovement
        self.ser.write(command.encode())
        

    def setThrottle(self, throttle):
        self.ser.write('t'.encode())        
        if throttle > 255:
            self.throttle = 255
        elif throttle <= 0:
            self.throttle = 100
        else:
            self.throttle = throttle
        print ("tje boy")
        print (throttle)
        byte = bytes([int(self.throttle)])
        print ("tje boy")
        print (byte)
        self.ser.write(byte)
        
    def printSerial(self):
        print(self.ser.read(self.ser.inWaiting()))
