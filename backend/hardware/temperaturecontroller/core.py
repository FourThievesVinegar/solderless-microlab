"""
This module contains the implementations of the temperature controller. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""
from hardware.temperaturecontroller.base import TempController
from hardware.temperaturecontroller.basictempcontroller import BasicTempController
from hardware.temperaturecontroller.simulation import SimulatedTempController


def createTemperatureController(tempControllerConfig: dict, devices: dict) -> TempController:
    tempControllerType = tempControllerConfig['implementation']
    if tempControllerType == 'basic':
        return BasicTempController(tempControllerConfig, devices)
    elif tempControllerType == 'simulation':
        return SimulatedTempController(tempControllerConfig)
    raise ValueError(
        'Unsupported device: id={config[id]} '
        'type={config[type]} implementation={config[implementation]}'.format(config=tempControllerConfig)
    )
