#!/usr/bin/python
import RPi.GPIO as GPIO
import time

class ProximityInterface(object):
    def __init__(self):

        # setup pins and such
        GPIO.setmode(GPIO.BOARD)

        self.PIN_TRIGGER = 12
        self.PIN_ECHO = 13

        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO, GPIO.IN)

        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

    def getProximity(self, trigger, echo):
        try:
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
        except:
            print("proximity error")
            return -1

    def getForwardProximity(self):
        return self.getProximity(self.PIN_TRIGGER, self.PIN_ECHO)

    def __del__(self):
        GPIO.cleanup()

    def close(self):
        GPIO.cleanup()
