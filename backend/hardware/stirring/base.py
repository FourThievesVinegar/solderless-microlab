from abc import ABC, abstractmethod


class Stirrer(ABC):
    @abstractmethod
    def turnStirrerOn(self):
        """
        Start stirrer.

        :return:
            None
        """
        pass

    @abstractmethod
    def turnStirrerOff(self):
        """
        Stop stirrer.

        :return:
            None
        """
        pass
