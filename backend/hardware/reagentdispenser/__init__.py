"""
The hardware package simply routes hardware calls to the appropriate python package that does the actual work.
The hardware package is configured in config.hardwarePackage and it must implement the methods as defined in
hardware.interface and used in this module below.
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
