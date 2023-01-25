from hardware.stirring.base import Stirrer

RELAY_ON = 1
RELAY_OFF = 0

class GPIOStirrer(Stirrer):
    stirrerPin = None

    def __init__(self, args, devices):
        """
        Constructor. Initializes the stirrer.
        :param args:
          dict
            stirrerPin
              Which gpio pin to control the stirrer
            gpioID
              The ID of the GPIO device used to control stirring
        """
        self.gpio = devices[args["gpioID"]]
        self.stirrerPin = args["stirrerPin"]
        
        self.gpio.setup(self.stirrerPin)
        self.gpio.output(self.stirrerPin, RELAY_OFF)

    def turnStirrerOn(self):
        """
        Turns the stirrer on.

        :return:
        None
        """
        self.gpio.output(self.stirrerPin, RELAY_ON)


    def turnStirrerOff(self):
        """
        Turns the stirrer off.

        :return:
        None
        """
        self.gpio.output(self.stirrerPin, RELAY_OFF)
