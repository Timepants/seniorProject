from MotorControl import MotorContol as Motor


class MotorInterface(object):
    def __init__(self):
        self.MC = Motor()

    def setSteering(self, steering):
        if steering > 0.5:
            if self.MC.getHeading() != self.MC.RIGHT:
                self.MC.sendCommand(self.MC.RIGHT)
        elif steering < -0.5:
            if self.MC.getHeading() != self.MC.LEFT:
                self.MC.sendCommand(self.MC.LEFT)
        else:
            if self.MC.getHeading() != self.MC.NOT_SET:
                self.MC.sendCommand(self.MC.CLEAR_HEADING)

    def setMovement(self, movement):
        if movement > 0.5:
            self.MC.sendCommand(self.MC.FORWARD)
        elif movement < -0.5:
            self.MC.sendCommand(self.MC.BACKWARD)
        else:
            self.MC.sendCommand(self.MC.CLEAR_MOVEMENT)
            self.MC.setThrottle(0)

    def setThrottle(self, throttle):
        if throttle >= -10 and throttle <= 10:
            self.setMovement(0)
        else:
            if throttle < 0:
                movement = -1
                throttle = throttle * -1
            elif throttle > 0:
                movement = 1
            else:
                movement = 0
            self.setThrottleAndMovement(throttle, movement)

    def setThrottleAndMovement(self, throttle, movement):
        if(self.getThrottle() - throttle < -10 or self.getThrottle() - throttle > 10):
            self.MC.setThrottle(throttle)
        if(self.getMovement() != movement): 
            self.setMovement(movement)

    def stop(self):
        self.MC.sendCommand(self.MC.CLEAR_ALL)
        self.MC.setThrottle(0)

    def getSteering(self):
        if self.MC.getHeading() == self.MC.RIGHT:
            return 1
        elif self.MC.getHeading() == self.MC.LEFT:
            return -1
        else:
            return 0

    def getThrottle(self):
        if self.MC.getThrottle() <= 11:
            return 0
        else:
            return self.MC.getThrottle()

    def getMovement(self):
        if self.MC.getMovement() == self.MC.FORWARD:
            return 1
        elif self.MC.getMovement() == self.MC.BACKWARD:
            return -1
        else:
            return 0

    def printSerial(self):
        self.MC.printSerial()