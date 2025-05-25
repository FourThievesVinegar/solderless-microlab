from typing import Any

from hardware.temperaturecontroller.base import TempController

RELAY_ON: int = 1
RELAY_OFF: int = 0


class BasicTempController(TempController):
    def __init__(self, temp_controller_config: dict[str, Any], devices: dict[str, Any]):
        """
        Constructor. Initializes the stirrer.
        :param temp_controller_config:
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
        super().__init__(temp_controller_config, devices)
        self.heaterPin = temp_controller_config['heaterPin']
        self.heaterPumpPin = temp_controller_config['heaterPumpPin']
        self.coolerPin = temp_controller_config['coolerPin']
        self.maxTemp = temp_controller_config['maxTemp']
        self.minTemp = temp_controller_config['minTemp']

        self.device: 'hardware.gpiochip.base.GPIOChip' = devices[temp_controller_config['gpioID']]
        self.device.setup(self.heaterPin)
        self.device.setup(self.heaterPumpPin)
        self.device.setup(self.coolerPin)
        self.device.output(self.heaterPin, RELAY_OFF)
        self.device.output(self.heaterPumpPin, RELAY_OFF)
        self.device.output(self.coolerPin, RELAY_OFF)

        self.thermometer: 'hardware.thermometer.base.TempSensor' = devices[temp_controller_config['thermometerID']]

    def turnHeaterOn(self) -> None:
        """
        Turns heater on.

        :return:
        None
        """
        self.logger.debug(self.t['turned-on-heat'])
        self.device.output(self.heaterPin, RELAY_ON)

    def turnHeaterOff(self) -> None:
        """
        Turns heater off.

        :return:
        None
        """
        self.logger.debug(self.t['turned-off-heat'])
        self.device.output(self.heaterPin, RELAY_OFF)

    def turnHeaterPumpOn(self) -> None:
        self.logger.debug(self.t['heat-pump-on'])
        self.device.output(self.heaterPumpPin, RELAY_ON)

    def turnHeaterPumpOff(self) -> None:
        self.logger.debug(self.t['heat-pump-off'])
        self.device.output(self.heaterPumpPin, RELAY_OFF)

    def turnCoolerOn(self) -> None:
        """
        Turn cooler on.

        :return:
        None
        """
        self.logger.debug(self.t['turned-on-cool'])
        self.device.output(self.coolerPin, RELAY_ON)

    def turnCoolerOff(self) -> None:
        """
        Turn cooler off.

        :return:
        None
        """
        self.logger.debug(self.t['turned-off-cool'])
        self.device.output(self.coolerPin, RELAY_OFF)

    def getTemp(self) -> float:
        """
        Read the temperature from the temperature sensor.
        :return:
        The temperature of the temperature sensor.
        """
        return self.thermometer.getTemp()

    def getMaxTemperature(self) -> float:
        return self.maxTemp

    def getMinTemperature(self) -> float:
        return self.minTemp

    def getPIDConfig(self) -> dict[str, Any]:
        return self.pidConfig
