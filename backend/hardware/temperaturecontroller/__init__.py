"""
This module contains the implementations of the temperature controller. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
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
