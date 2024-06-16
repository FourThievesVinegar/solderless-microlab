import config
import hardware.thermometer as therm
from hardware.temperaturecontroller.base import TempController
import logging


RELAY_ON = 1
RELAY_OFF = 0

class BasicTempController(TempController):
    def __init__(self, args, devices):
        """
        Constructor. Initializes the stirrer.
        :param args:
          dict
            heaterPin
              Which gpio pin to control the heating element
            heaterPumpPin
              Which gpio pin to control the heater pump
            coolerPin
              Which gpio pin to control the cooler pump
            gpioID
              The ID of the GPIO device used to control heating and cooling
            maxTemp
              Maximum temperature the hardware will support
            minTemp
              Minimum temperature the hardware will support
        """
        super().__init__(args, devices)
        self.gpio = devices[args["gpioID"]]
        self.heaterPin = args["heaterPin"]
        self.heaterPumpPin = args["heaterPumpPin"]
        self.coolerPin = args["coolerPin"]
        self.maxTemp = args["maxTemp"]
        self.minTemp = args["minTemp"]

        self.gpio.setup(self.heaterPin)
        self.gpio.setup(self.heaterPumpPin)
        self.gpio.setup(self.coolerPin)

        self.gpio.output(self.heaterPin, RELAY_OFF)
        self.gpio.output(self.heaterPumpPin, RELAY_OFF)
        self.gpio.output(self.coolerPin, RELAY_OFF)

        self.thermometer = devices[args['thermometerID']]

    def turnHeaterOn(self):
        """
        Turns heater on.

        :return:
        None
        """
        logging.info("heater turned on")
        self.gpio.output(self.heaterPin, RELAY_ON)


    def turnHeaterOff(self):
        """
        Turns heater off.

        :return:
        None
        """
        logging.info("heater turned off")
        self.gpio.output(self.heaterPin, RELAY_OFF)

    def turnHeaterPumpOn(self):
        logging.info("heater pump turned on")
        self.gpio.output(self.heaterPumpPin, RELAY_ON)

    def turnHeaterPumpOff(self):
        logging.info("heater pump turned off")
        self.gpio.output(self.heaterPumpPin, RELAY_OFF)

    def turnCoolerOn(self):
        """
        Turn cooler on.

        :return:
        None
        """
        logging.info("cooler turned on")
        self.gpio.output(self.coolerPin, RELAY_ON)


    def turnCoolerOff(self):
        """
        Turn cooler off.

        :return:
        None
        """
        logging.info("cooler turned off")
        self.gpio.output(self.coolerPin, RELAY_OFF)


    def getTemp(self):
        """
        Read the temperature from the temperature sensor.
        :return:
        The temperature of the temperature sensor.
        """
        return self.thermometer.getTemp()
        
    def getMaxTemperature(self):
        return self.maxTemp

    def getMinTemperature(self):
        return self.minTemp

    def getPIDConfig(self):
        return self.pidConfig

