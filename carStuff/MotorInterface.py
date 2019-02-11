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

    def setThrottle(self, throttle):
        self.MC.setThrottle(throttle)
        self.MC.sendCommand(self.MC.FORWARD)

    def stop(self, throttle):
        self.MC.sendCommand(self.MC.CLEAR_ALL)

    def getSteering(self):
        if self.MC.getHeading() == self.MC.RIGHT:
            return 1
        elif self.MC.getHeading() == self.MC.LEFT:
            return -1
        else:
            return 0