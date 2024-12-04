from hardware.grbl.base import GRBL

class GRBLSimulation(GRBL):
    def __init__(self, grbl_config: dict):
        """
        Constructor. GRBLSimulation does nothing so needs no configuration.
        """
        pass

    def grblWrite(self, command: str, retries=3):
        pass
