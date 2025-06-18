from hardware.grbl.base import GRBL

class GRBLSimulation(GRBL):
    def __init__(self, grbl_config: dict):
        """
        Constructor. GRBLSimulation does nothing so need no configuration.
        """
        super().__init__('simulation')

    def write_gcode(self, command: str, retries: int = 3) -> None:
        """ :inheritdoc: """
        pass
