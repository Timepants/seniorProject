from MotorControl import MotorContol as Motor


class MotorInterface(object):
    def __init__(self):
        self.MC = Motor()

    def setSteering(self, steering):
        if steering > 0.5:
            self.MC.sendCommand(self.MC.RIGHT)
        elif steering < -0.5:
            self.MC.sendCommand(self.MC.LEFT)
        else:
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
        self.MC.setThrottle(throttle)
        self.MC.sendCommand(self.MC.FORWARD)

    def setThrottle(self, throttle, movement):
        self.MC.setThrottle(throttle)
        self.setMovement(movement)

    def stop(self):
        self.MC.sendCommand(self.MC.CLEAR_ALL)
        self.MC.setThrottle(0)

    def getSteering(self):
        if self.MC.getHeading() == self.MC.RIGHT:
            return 7
        elif self.MC.getHeading() == self.MC.LEFT:
            return -7
        else:
            return 0

    def getThrottle(self):
        if self.MC.getThrottle() <= 11:
            return 0
        else:
            return self.MC.getThrottle()

    def getMovement(self):
        if self.MC.getMovement() == self.MC.FORWARD:
            return 7
        elif self.MC.getMovement() == self.MC.BACKWARD:
            return -7
        else:
            return 0

    def printSerial(self):
        self.MC.printSerial()