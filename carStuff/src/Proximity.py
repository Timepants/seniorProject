#!/usr/bin/python
import RPi.GPIO as GPIO
import time

class ProximityInterface(object):
    def __init__(self):

        # setup pins and such
        GPIO.setmode(GPIO.BOARD)

        self.PIN_TRIGGER_FORWARD = 7
        self.PIN_ECHO_FORWARD = 11

        self.PIN_TRIGGER_BACKWARD = 12
        self.PIN_ECHO_BACKWARD = 13
        GPIO.setup(self.PIN_TRIGGER_FORWARD, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO_FORWARD, GPIO.IN)

        GPIO.setup(self.PIN_TRIGGER_BACKWARD, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO_BACKWARD, GPIO.IN)

        GPIO.output(self.PIN_TRIGGER_FORWARD, GPIO.LOW)
        GPIO.output(self.PIN_TRIGGER_BACKWARD, GPIO.LOW)

    def getProximity(self, trigger, echo):

        # send the signal
        GPIO.output(trigger, GPIO.HIGH)

        time.sleep(0.00001)

        # stop sending
        GPIO.output(trigger, GPIO.LOW)

        # get the times from echo
        while GPIO.input(echo)==0:
            pulse_start_time = time.time()

        while GPIO.input(echo)==1:
            pulse_end_time = time.time()


        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        return distance

    def getForwardProximity(self):
        return self.getProximity(self.PIN_TRIGGER_FORWARD, self.PIN_ECHO_FORWARD)

    def getBackwardProximity(self):
        return self.getProximity(self.PIN_TRIGGER_BACKWARD, self.PIN_ECHO_BACKWARD)

    def __del__(self):
        GPIO.cleanup()

    def close(self):
        GPIO.cleanup()

# TODO remove test code

prox = ProximityInterface()

prox.getForwardProximity()

prox.getBackwardProximity()