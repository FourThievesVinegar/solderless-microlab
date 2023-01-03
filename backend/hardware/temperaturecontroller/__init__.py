"""
The hardware package simply routes hardware calls to the appropriate python package that does the actual work.
The hardware package is configured in config.hardwarePackage and it must implement the methods as defined in
hardware.interface and used in this module below.
"""

import config
from hardware.temperaturecontroller.basictempcontroller import BasicTempController
from hardware.temperaturecontroller.simulation import SimulatedTempController

def createTemperatureController(tempControllerType, args):
    if tempControllerType == "basic":
        return BasicTempController(args)
    elif tempControllerType == "simulation":
        return SimulatedTempController(args)
    raise "Unsupported tempControllerType"