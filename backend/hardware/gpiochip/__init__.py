"""
This module contains the implementations for gpio control. See base.py for the abstract class used
and the individual files for configuration information.
"""

def createGPIOChip(gpioConfig, devices):
    gpioType = gpioConfig['implementation']
    if gpioType == "gpiod":
        from hardware.gpiochip.gpiod import GPIODChip
        return GPIODChip(gpioConfig)
    if gpioType == "simulation":
        from hardware.gpiochip.gpiod_simulation import GPIODChipSimulation
        return GPIODChipSimulation(gpioConfig)
    raise Exception("Unsupported gpiochiptype")
