from hardware.stirring.base import Stirrer


class SimulatedStirrer(Stirrer):
    def __init__(self) -> None:
        super().__init__('simulation')

    def turn_stirrer_on(self) -> None:
        """ :inheritdoc: """
        return None

    def turn_stirrer_off(self) -> None:
        """ :inheritdoc: """
        return None

    def close(self) -> None:
        pass
