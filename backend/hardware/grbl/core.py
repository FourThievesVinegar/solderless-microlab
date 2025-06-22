"""
This module contains the implementations for grbl control. See base.py for the abstract class used
and the individual files for configuration information.
"""
from typing import Any

from hardware.grbl.base import GRBL
from hardware.lab_device import LabDevice


def create_grbl(device_config: dict[str, Any], devices: dict[str, LabDevice]) -> GRBL:
    grbl_type = device_config['implementation']
    if grbl_type == 'serial':
        from hardware.grbl.serial import GRBLSerial
        return GRBLSerial(device_config)
    if grbl_type == 'simulation':
        from hardware.grbl.simulation import GRBLSimulation
        return GRBLSimulation(device_config)
    raise ValueError(
        'Unsupported device: id={config[id]} '
        'type={config[type]} implementation={config[implementation]}'.format(config=device_config)
    )
