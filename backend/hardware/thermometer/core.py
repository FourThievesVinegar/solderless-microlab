"""
This module contains the implementations of the thermometer. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""
from hardware.thermometer.base import TempSensor


def createThermometer(thermometerConfig: dict, devices: dict) -> TempSensor:
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
    raise Exception('Unsupported thermometer type')
