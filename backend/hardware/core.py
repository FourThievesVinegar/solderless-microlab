"""
The hardware package acts as the interface for the software to interact with any hardware. Currently split into 3 different
distinct modules, the temperature controller, stirrer, and reagent dispenser, which contain the functions needed for 
controller the temperature of the reactor, stirring, and dispensing any reagents into the microlab respectively.
Alternative implementations just need to implement a new class withthe functions of the base class in the base.py file 
for the module, as well as adding a call to that for a unique string setting to the create function in the __init__.py
file.
"""

import logging
import time
import config
from hardware import devicelist
from enum import Enum
from util.logger import MultiprocessingLogger

from hardware.devicelist import loadHardwareConfiguration


class MicroLabHardwareState(Enum):
    STARTING = "STARTING"
    INITIALIZED = "INITIALIZED"
    FAILED_TO_START = "FAILED_TO_START"


class MicroLabHardware:

    _microlabHardware = None
    _logger = None

    def __init__(self, deviceDefinition: list[dict]):
        """
        Constructor. Initializes the hardware.
        """

        self.startTime = None
        self.devices = {}
        self.state = MicroLabHardwareState.STARTING
        self.error = None
    
        self.startTime = time.monotonic()
        self.loadHardware(deviceDefinition)

        if self._logger is None:
            self._logger = self._get_logger()

    @classmethod
    def _get_logger(cls) -> logging.Logger:
        return MultiprocessingLogger.get_logger(__name__)

    @classmethod
    def get_microlab_hardware_controller(cls):
        if cls._logger is None:
            cls._logger = cls._get_logger()

        if not cls._microlabHardware:
            cls._logger.info("")
            cls._logger.info("### STARTING MICROLAB HARDWARE CONTROLLER ###")
            cls._logger.info("Loading microlab hardware configuration.")

            hardwareConfig = loadHardwareConfiguration()
            deviceDefinitions = hardwareConfig['devices']
            cls._microlabHardware = MicroLabHardware(deviceDefinitions)

        return cls._microlabHardware

    def loadHardware(self, deviceDefinition: list[dict]):
        """
        Loads and initializes the hardware devices

        :return:
            (True, '') on success.
            (False, message) on failure.
        """
        try:
            self.devices = devicelist.setupDevices(deviceDefinition)
            self.tempController = self.devices['reactor-temperature-controller']
            self.stirrer = self.devices['reactor-stirrer']
            self.reagentDispenser = self.devices['reactor-reagent-dispenser']
            self.state = MicroLabHardwareState.INITIALIZED
            return True, ''
        except Exception as e:
            self._logger.exception(str(e))
            self.state = MicroLabHardwareState.FAILED_TO_START
            self.error = e
            return False, str(e)

    def turnOffEverything(self):
        """
        Stops any running hardware

        :return:
        None
        """
        self.turnHeaterOff()
        self.turnHeaterPumpOff()
        self.turnCoolerOff()
        self.turnStirrerOff()

    def secondSinceStart(self):
        """
        The number of seconds since this package was started multiplied by config.hardwareSpeedup.

        This can effectively simulate time speedups for testing recipes.

        :return:
        The number of seconds since this package was started multiplied by config.hardwareSpeedup.
        """
        elapsed = time.monotonic() - self.startTime
        if hasattr(config,'hardwareSpeedup'):
            speed = config.hardwareSpeedup
            if not (speed == None):
                return elapsed * speed

        return elapsed

    def sleep(self, seconds):
        """
        Sleep for a number of seconds or if config.harwareSpeedup is configured, for a number of
        seconds/config.hardwareSpeedup

        The point of this method is to allow for speeding up time without modifying the recipes. This
        is especially useful for testing.

        :param seconds:
        Number of seconds to sleep. In real life will actually sleep for seconds/config.hardwareSpeedup.

        :return:
        None
        """
        if hasattr(config, 'hardwareSpeedup'):
            speed = config.hardwareSpeedup
            if not (speed is None):
                time.sleep(seconds/speed)
                return

        time.sleep(seconds)

    def getMaxTemperature(self):
        """
        :return:
        The max allowed temperature of the microlab in celsius as a number
        """
        return self.tempController.getMaxTemperature()

    def getMinTemperature(self):
        """
        :return:
        The minimum allowed temperature of the microlab in celsius as a number
        """
        return self.tempController.getMinTemperature()

    def turnHeaterOn(self):
        """
        Start heating the jacket.

        :return:
            None
        """
        self.tempController.turnCoolerOff()
        self.tempController.turnHeaterOn()

    def turnHeaterOff(self):
        """
        Stop heating the jacket.

        :return:
            None
        """
        self.tempController.turnHeaterOff()

    def turnHeaterPumpOn(self):
        """
        Turns on the heater pump.

        :return:
            None
        """
        self.tempController.turnHeaterPumpOn()

    def turnHeaterPumpOff(self):
        """
        Turns off the heater pump.

        :return:
            None
        """
        self.tempController.turnHeaterPumpOff()

    def turnCoolerOn(self):
        """
        Start cooling the jacket.

        :return:
            None
        """
        self.tempController.turnHeaterOff()
        self.tempController.turnCoolerOn()

    def turnCoolerOff(self):
        """
        Stop cooling the jacket.

        :return:
            None
        """
        self.tempController.turnCoolerOff()

    def turnStirrerOn(self):
        """
        Start stirrer.

        :return:
            None
        """
        self.stirrer.turnStirrerOn()

    def turnStirrerOff(self):
        """
        Start stirrer.

        :return:
            None
        """
        self.stirrer.turnStirrerOff()

    def getTemp(self):
        """
        Return the temperature.

        :return:
            The temperature as read from the sensor in Celsius
        """
        return self.tempController.getTemp()

    def getPIDConfig(self):
        """
        Return the temperature.

        :return:
            The temperature as read from the sensor in Celsius
        """
        return self.tempController.getPIDConfig()

    def pumpDispense(self, pumpId, volume, duration=None):
        """
        Dispense a number of ml from a particular pump.

        :param pumpId:
            The pump id. One of 'X', 'Y' or 'Z'
        :param volume:
            The number ml to dispense
        :param duration:
            optional - How long the dispense should take in seconds
        :return:
            Number indicating how long the dispense should take to complete
        """
        return self.reagentDispenser.dispense(pumpId, volume, duration)

    def getPumpSpeedLimits(self, pumpId):
        """
        Get maximum and minimum speed of specified pump.

        :param pumpId:
            The pump id. One of 'X' or 'Y' or 'Z'
        :return:
            dict
                minSpeed
                    Minimum speed the pump can dispense in ml/s
                maxSpeed
                    Maximum speed the pump can dispense in ml/s
        """
        return self.reagentDispenser.getPumpSpeedLimits(pumpId)
