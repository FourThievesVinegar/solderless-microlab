from hardware.stirring.base import Stirrer


class SimulatedStirrer(Stirrer):
    def turnStirrerOn(self) -> None:
        """
        Start stirrer.

        :return:
            None
        """
        return None

    def turnStirrerOff(self) -> None:
        """
        Stop stirrer.

        :return:
            None
        """
        return None
