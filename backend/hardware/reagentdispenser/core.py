"""
This module contains the implementations of the reagent dispenser. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""
from hardware.reagentdispenser.base import ReagentDispenser
from hardware.reagentdispenser.peristalticpump import PeristalticPump
from hardware.reagentdispenser.syringepump import SyringePump
from hardware.reagentdispenser.simulation import SimulatedReagentDispenser


def createReagentDispenser(reagentdispenserConfig: dict, devices: dict) -> ReagentDispenser:
    reagentdispenserType = reagentdispenserConfig['implementation']
    if reagentdispenserType == 'syringepump':
        return SyringePump(reagentdispenserConfig, devices)
    elif reagentdispenserType == 'peristalticpump':
        return PeristalticPump(reagentdispenserConfig, devices)
    elif reagentdispenserType == 'simulation':
        return SimulatedReagentDispenser(reagentdispenserConfig)
    raise ValueError(
        'Unsupported device: id={config[id]} '
        'type={config[type]} implementation={config[implementation]}'.format(config=reagentdispenserConfig)
    )
