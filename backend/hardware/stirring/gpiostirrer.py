import RPi.GPIO as GPIO
from hardware.stirring.base import Stirrer

RELAY_ON = True
RELAY_OFF = False

class GPIOStirrer(Stirrer):
    stirrerPin = None

    def __init__(self, args):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.stirrerPin = args["stirrerPin"]
        
        GPIO.setup(self.stirrerPin, GPIO.OUT)
        GPIO.output(self.stirrerPin, RELAY_OFF)

    def turnStirrerOn(self):
        """
        Turns the stirrer on.

        :return:
        None
        """
        GPIO.output(self.stirrerPin, RELAY_ON)


    def turnStirrerOff(self):
        """
        Turns the stirrer off.

        :return:
        None
        """
        GPIO.output(self.stirrerPin, RELAY_OFF)
