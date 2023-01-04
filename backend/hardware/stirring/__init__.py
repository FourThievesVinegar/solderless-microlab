"""
This module contains the implementations of the stirrer. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""

from hardware.stirring.gpiostirrer import GPIOStirrer
from hardware.stirring.simulation import SimulatedStirrer

def createStirrer(stirrerType, args):
    if stirrerType == "gpio_stirrer":
        return GPIOStirrer(args)
    elif stirrerType == "simulation":
        return SimulatedStirrer()
    raise "Unsupported stirrerType"
