"""
This module contains the implementations of the reagent dispenser. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""

from hardware.reagentdispenser.syringepump import SyringePump
from hardware.reagentdispenser.simulation import SimulatedReagentDispenser

def createReagentDispenser(reagentdispenserType, args):
    if reagentdispenserType == "syringepump":
        print(args)
        return SyringePump(args)
    elif reagentdispenserType == "simulation":
        return SimulatedReagentDispenser()
    raise "Unsupported reagentdispenserType"
