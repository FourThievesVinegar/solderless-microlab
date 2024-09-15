from hardware.stirring.base import Stirrer


class SimulatedStirrer(Stirrer):
    def turnStirrerOn(self):
        """
        Start stirrer.

        :return:
            None
        """
        return None

    def turnStirrerOff(self):
        """
        Stop stirrer.

        :return:
            None
        """
        return None
