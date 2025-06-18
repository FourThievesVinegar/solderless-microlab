"""
This module contains the implementations of the stirrer. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""
from typing import Any

from hardware.stirring.base import Stirrer
from hardware.util.lab_device_type import LabDevice


def create_stirrer(device_config: dict[str, Any], devices: dict[str, LabDevice]) -> Stirrer:
    stirrer_type = device_config['implementation']
    if stirrer_type == 'gpio_stirrer':
        from hardware.stirring.gpiostirrer import GPIOStirrer
        return GPIOStirrer(device_config, devices)
    elif stirrer_type == 'simulation':
        from hardware.stirring.simulation import SimulatedStirrer
        return SimulatedStirrer()
    raise ValueError(
        'Unsupported device: id={config[id]} '
        'type={config[type]} implementation={config[implementation]}'.format(config=device_config)
    )
