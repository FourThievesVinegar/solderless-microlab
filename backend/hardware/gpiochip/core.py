"""
This module contains the implementations for gpio control. See base.py for the abstract class used
and the individual files for configuration information.
"""


def createGPIOChip(gpioConfig: dict, devices: dict):
    gpioType = gpioConfig['implementation']
    if gpioType == "gpiod":
        from hardware.gpiochip.gpiod import GPIODChip
        return GPIODChip(gpioConfig)
    if gpioType == "simulation":
        from hardware.gpiochip.gpiod_simulation import GPIODChipSimulation
        return GPIODChipSimulation(gpioConfig)
    if gpioType == "gpiod_chipset":
        from hardware.gpiochip.gpiod_chipset import GPIODChipset
        return GPIODChipset(gpioConfig, devices)
    if gpioType == "grbl":
        from hardware.gpiochip.grbl import GRBLChip
        return GRBLChip(gpioConfig, devices)
    raise Exception("Unsupported gpiochiptype")
