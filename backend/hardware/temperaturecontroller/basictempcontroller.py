import config
import RPi.GPIO as GPIO
import hardware.thermometer as therm
from hardware.temperaturecontroller.base import TempController


RELAY_ON = True
RELAY_OFF = False

class BasicTempController(TempController):
    thermometer = None
    heaterPin = None
    heaterPumpPin = None
    coolerPin = None
    def __init__(self, args):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.heaterPin = args["heaterPin"]
        self.heaterPumpPin = args["heaterPumpPin"]
        self.coolerPin = args["coolerPin"]

        GPIO.setup(self.heaterPin, GPIO.OUT)
        GPIO.setup(self.heaterPumpPin, GPIO.OUT)
        GPIO.setup(self.coolerPin, GPIO.OUT)

        GPIO.output(self.heaterPin, RELAY_OFF)
        GPIO.output(self.heaterPumpPin, RELAY_OFF)
        GPIO.output(self.coolerPin, RELAY_OFF)

        self.thermometer = therm.createThermometer(args["thermometerType"], args["thermometerArgs"])

    def turnHeaterOn(self):
        """
        Turns heater on.

        :return:
        None
        """
        print("heater turned on")
        GPIO.output(self.heaterPin, RELAY_ON)
        GPIO.output(self.heaterPumpPin, RELAY_ON)


    def turnHeaterOff(self):
        """
        Turns heater off.

        :return:
        None
        """
        print("heater turned off")
        GPIO.output(self.heaterPin, RELAY_OFF)
        GPIO.output(self.heaterPumpPin, RELAY_OFF)


    def turnCoolerOn(self):
        """
        Turn cooler on.

        :return:
        None
        """
        print("cooler turned on")
        GPIO.output(self.coolerPin, RELAY_ON)


    def turnCoolerOff(self):
        """
        Turn cooler off.

        :return:
        None
        """
        print("cooler turned off")
        GPIO.output(self.coolerPin, RELAY_OFF)


    def getTemp(self):
        """
        Read the temperature from the temperature sensor.
        :return:
        The temperature of the temperature sensor.
        """
        return self.thermometer.getTemp()
