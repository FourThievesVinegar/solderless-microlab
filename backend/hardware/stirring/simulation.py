from hardware.stirring.base import Stirrer


class SimulatedStirrer(Stirrer):
    def __init__(self) -> None:
        super().__init__('simulation')

    def turnStirrerOn(self) -> None:
        """ :inheritdoc: """
        return None

    def turnStirrerOff(self) -> None:
        """ :inheritdoc: """
        return None
