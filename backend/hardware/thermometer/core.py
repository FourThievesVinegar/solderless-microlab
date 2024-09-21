"""
This module contains the implementations of the thermometer. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""

from hardware.thermometer.serial import SerialTempSensor
from hardware.thermometer.serial_simulation import SerialTempSensorSimulation

W1_IMPORT_ERROR = False

try:
    from w1thermsensor import W1ThermSensor
except Exception:
    # We have to catch broadly for this exception as there is an error defined
    # in the w1thermsensor library to attempt to catch this issue
    # however the exception is triggered on any module import as
    # the load is attempted in the __init__ file in the base of the repo
    # so no imports will work at all if there is a load error
    W1_IMPORT_ERROR = True
else:
    from hardware.thermometer.w1_therm import W1TempSensor


def createThermometer(thermometerConfig: dict, devices: dict):
    thermometerType = thermometerConfig['implementation']
    if thermometerType == "w1_therm" and not W1_IMPORT_ERROR:
        return W1TempSensor()
    elif thermometerType == "serial":
        return SerialTempSensor(thermometerConfig)
    elif thermometerType == "simulation":
        return SerialTempSensorSimulation(thermometerConfig)
    raise Exception("Unsupported thermometer type")
