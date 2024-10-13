from hardware.stirring.base import Stirrer
import sys


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
        sys.stdout.write('Turning off stirrer in SimulatedStirrer\n')
        sys.stdout.flush()

        return None
