"""
This module contains the implementations for grbl control. See base.py for the abstract class used
and the individual files for configuration information.
"""
from localization import load_translation

def createGRBL(grblConfig: dict, _devices: dict):
    t=load_translation()
    grblType = grblConfig['implementation']
    if grblType == "serial":
        from hardware.grbl.serial import GRBLSerial
        return GRBLSerial(grblConfig)
    if grblType == "simulation":
        from hardware.grbl.simulation import GRBLSimulation
        return GRBLSimulation(grblConfig)
    raise Exception(t['unsupported-grbl-type'])
