"""
This module contains the implementations of the stirrer. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""
from hardware.stirring.base import Stirrer
from hardware.stirring.gpiostirrer import GPIOStirrer
from hardware.stirring.simulation import SimulatedStirrer


def createStirrer(stirrerConfig: dict, devices: dict) -> Stirrer:
    stirrerType = stirrerConfig['implementation']
    if stirrerType == 'gpio_stirrer':
        return GPIOStirrer(stirrerConfig, devices)
    elif stirrerType == 'simulation':
        return SimulatedStirrer()
    raise ValueError(
        'Unsupported device: id={config[id]} '
        'type={config[type]} implementation={config[implementation]}'.format(config=stirrerConfig)
    )
