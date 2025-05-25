"""
This module contains the implementations of the Thermometer. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""
from typing import Any

from hardware.thermometer.base import TempSensor


def createThermometer(thermometerConfig: dict[str, Any], devices: dict[str, Any]) -> TempSensor:
    thermometerType = thermometerConfig['implementation']
    if thermometerType == 'w1_therm':
        from hardware.thermometer.w1_therm import W1TempSensor
        return W1TempSensor()
    elif thermometerType == 'serial':
        from hardware.thermometer.serial import SerialTempSensor
        return SerialTempSensor(thermometerConfig)
    elif thermometerType == 'simulation':
        from hardware.thermometer.serial_simulation import SerialTempSensorSimulation
        return SerialTempSensorSimulation(thermometerConfig)
    raise ValueError(
        'Unsupported device: id={config[id]} '
        'type={config[type]} implementation={config[implementation]}'.format(config=thermometerConfig)
    )
