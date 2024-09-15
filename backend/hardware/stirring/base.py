from abc import ABC, abstractmethod


class Stirrer(ABC):
    @abstractmethod
    def turnStirrerOn():
        """
        Start stirrer.

        :return:
            None
        """
        pass

    @abstractmethod
    def turnStirrerOff():
        """
        Stop stirrer.

        :return:
            None
        """
        pass
