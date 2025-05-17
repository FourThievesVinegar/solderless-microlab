"""
This module contains the implementations for grbl control. See base.py for the abstract class used
and the individual files for configuration information.
"""
from hardware.grbl.base import GRBL


def createGRBL(grbl_config: dict, devices: dict) -> GRBL:
    grblType = grbl_config['implementation']
    if grblType == 'serial':
        from hardware.grbl.serial import GRBLSerial
        return GRBLSerial(grbl_config)
    if grblType == 'simulation':
        from hardware.grbl.simulation import GRBLSimulation
        return GRBLSimulation(grbl_config)
    raise ValueError(
        'Unsupported chip: id={config[id]} name={config[chipName]} '
        'type={config[type]} implementation={config[implementation]}'.format(config=grbl_config)
    )