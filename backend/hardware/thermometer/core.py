"""
This module contains the implementations of the thermometer. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""

from hardware.thermometer.w1_therm import W1TempSensor
from hardware.thermometer.serial import SerialTempSensor
from hardware.thermometer.serial_simulation import SerialTempSensorSimulation


def createThermometer(thermometerConfig: dict, devices: dict):
    thermometerType = thermometerConfig['implementation']
    if thermometerType == "w1_therm":
        return W1TempSensor()
    elif thermometerType == "serial":
        return SerialTempSensor(thermometerConfig)
    elif thermometerType == "simulation":
        return SerialTempSensorSimulation(thermometerConfig)
    raise Exception("Unsupported thermometer type")
