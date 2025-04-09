"""
This module contains the implementations of the reagent dispenser. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""
from hardware.reagentdispenser.peristalticpump import PeristalticPump
from hardware.reagentdispenser.syringepump import SyringePump
from hardware.reagentdispenser.simulation import SimulatedReagentDispenser

from localization import load_translation

def createReagentDispenser(reagentdispenserConfig: dict, devices: dict):
    t=load_translation()
    
    reagentdispenserType = reagentdispenserConfig['implementation']
    if reagentdispenserType == "syringepump":
        return SyringePump(reagentdispenserConfig, devices)
    elif reagentdispenserType == "peristalticpump":
        return PeristalticPump(reagentdispenserConfig, devices)
    elif reagentdispenserType == "simulation":
        return SimulatedReagentDispenser(reagentdispenserConfig)
    raise Exception(t['unsupported-reagent-dispenser-type'])
