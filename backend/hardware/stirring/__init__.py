"""
The hardware package simply routes hardware calls to the appropriate python package that does the actual work.
The hardware package is configured in config.hardwarePackage and it must implement the methods as defined in
hardware.interface and used in this module below.
"""

from hardware.stirring.gpiostirrer import GPIOStirrer
from hardware.stirring.simulation import SimulatedStirrer

def createStirrer(stirrerType, args):
    if stirrerType == "gpio_stirrer":
        return GPIOStirrer(args)
    elif stirrerType == "simulation":
        return SimulatedStirrer()
    raise "Unsupported stirrerType"
