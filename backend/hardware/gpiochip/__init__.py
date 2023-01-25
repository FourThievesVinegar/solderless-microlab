"""
This module contains the implementations for gpio control. See base.py for the abstract class used
and the individual files for configuration information.
"""
from hardware.gpiochip.gpiod import GPIODChip

def createGPIOChip(gpioConfig, devices):
    gpioType = gpioConfig['implementation']
    if gpioType == "gpiod":
        return GPIODChip(gpioConfig)
    raise Exception("Unsupported gpiochiptype")
