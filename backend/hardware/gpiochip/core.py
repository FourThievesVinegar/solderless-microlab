"""
This module contains the implementations for gpio control. See base.py for the abstract class used
and the individual files for configuration information.
"""

from hardware.gpiochip.gpiod_simulation import GPIODChipSimulation
from hardware.gpiochip.gpiod_chipset import GPIODChipset

IMPORT_ERROR = False

# We check for an import error here as this ikmport requires the gpiod python library
# to be installed, which is not a requirement
try:
    from hardware.gpiochip.gpiod import GPIODChip
except ModuleNotFoundError:
    IMPORT_ERROR = True


def createGPIOChip(gpioConfig: dict, devices: dict):
    gpioType = gpioConfig['implementation']
    if gpioType == "gpiod" and not IMPORT_ERROR:
        return GPIODChip(gpioConfig)
    if gpioType == "simulation":
        return GPIODChipSimulation(gpioConfig)
    if gpioType == "gpiod_chipset":
        return GPIODChipset(gpioConfig, devices)
    raise Exception("Unsupported gpiochiptype")
