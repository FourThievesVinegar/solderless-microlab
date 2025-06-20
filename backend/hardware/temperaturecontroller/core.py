"""
This module contains the implementations of the temperature controller. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""
from typing import Any

from hardware.temperaturecontroller.base import TempController
from hardware.lab_device import LabDevice


def create_temperature_controller(device_config: dict[str, Any], devices: dict[str, LabDevice]) -> TempController:
    controller_type = device_config['implementation']
    if controller_type == 'basic':
        from hardware.temperaturecontroller.basictempcontroller import BasicTempController
        return BasicTempController(device_config, devices)
    elif controller_type == 'simulation':
        from hardware.temperaturecontroller.simulation import SimulatedTempController
        return SimulatedTempController(device_config)
    raise ValueError(
        'Unsupported device: id={config[id]} '
        'type={config[type]} implementation={config[implementation]}'.format(config=device_config)
    )
