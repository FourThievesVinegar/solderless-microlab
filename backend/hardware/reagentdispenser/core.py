"""
This module contains the implementations of the reagent dispenser. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""
from typing import Any

from hardware.reagentdispenser.base import ReagentDispenser
from hardware.util.lab_device_type import LabDevice


def create_reagent_dispenser(device_config: dict[str, Any], devices: dict[str, LabDevice]) -> ReagentDispenser:
    dispenser_type = device_config['implementation']
    if dispenser_type == 'syringepump':
        from hardware.reagentdispenser.syringepump import SyringePump
        return SyringePump(device_config, devices)
    elif dispenser_type == 'peristalticpump':
        from hardware.reagentdispenser.peristalticpump import PeristalticPump
        return PeristalticPump(device_config, devices)
    elif dispenser_type == 'simulation':
        from hardware.reagentdispenser.simulation import SimulatedReagentDispenser
        return SimulatedReagentDispenser(device_config)
    raise ValueError(
        'Unsupported device: id={config[id]} '
        'type={config[type]} implementation={config[implementation]}'.format(config=device_config)
    )
