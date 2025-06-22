from typing import Any

from hardware.temperaturecontroller.base import TempController
from hardware.lab_device import LabDevice

RELAY_ON: int = 1
RELAY_OFF: int = 0


class BasicTempController(TempController):
    def __init__(self, temp_controller_config: dict[str, Any], devices: dict[str, LabDevice]):
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
        self.heater_pin = temp_controller_config['heaterPin']
        self.heater_pump_pin = temp_controller_config['heaterPumpPin']
        self.cooler_pin = temp_controller_config['coolerPin']
        self.max_temp = temp_controller_config['maxTemp']
        self.min_temp = temp_controller_config['minTemp']

        self.device: 'hardware.gpiochip.base.GPIOChip' = devices[temp_controller_config['gpioID']]
        self.device.setup(self.heater_pin)
        self.device.setup(self.heater_pump_pin)
        self.device.setup(self.cooler_pin)
        self.device.output(self.heater_pin, RELAY_OFF)
        self.device.output(self.heater_pump_pin, RELAY_OFF)
        self.device.output(self.cooler_pin, RELAY_OFF)

        self.thermometer: 'hardware.thermometer.base.TempSensor' = devices[temp_controller_config['thermometerID']]

    def turn_heater_on(self) -> None:
        """ Turns heater on. """
        self.logger.debug(self.t['turned-on-heat'])
        self.device.output(self.heater_pin, RELAY_ON)

    def turn_heater_off(self) -> None:
        """ Turns heater off. """
        self.logger.debug(self.t['turned-off-heat'])
        self.device.output(self.heater_pin, RELAY_OFF)

    def turn_heater_pump_on(self) -> None:
        self.logger.debug(self.t['heat-pump-on'])
        self.device.output(self.heater_pump_pin, RELAY_ON)

    def turn_heater_pump_off(self) -> None:
        self.logger.debug(self.t['heat-pump-off'])
        self.device.output(self.heater_pump_pin, RELAY_OFF)

    def turn_cooler_on(self) -> None:
        """ Turn cooler on. """
        self.logger.debug(self.t['turned-on-cool'])
        self.device.output(self.cooler_pin, RELAY_ON)

    def turn_cooler_off(self) -> None:
        """ Turn cooler off. """
        self.logger.debug(self.t['turned-off-cool'])
        self.device.output(self.cooler_pin, RELAY_OFF)

    def get_temp(self) -> float:
        """
        Read the temperature from the temperature sensor.
        :return:
            The temperature of the temperature sensor.
        """
        return self.thermometer.get_temp()

    def get_max_temperature(self) -> float:
        return self.max_temp

    def get_min_temperature(self) -> float:
        return self.min_temp

    def get_pid_config(self) -> dict[str, Any]:
        return self.pid_config

    def close(self) -> None:
        self.device.close()
        self.thermometer.close()