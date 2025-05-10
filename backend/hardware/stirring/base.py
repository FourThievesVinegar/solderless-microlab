from abc import ABC, abstractmethod


class Stirrer(ABC):
    @abstractmethod
    def turnStirrerOn(self) -> None:
        """
        Start stirrer.

        :return:
            None
        """
        pass

    @abstractmethod
    def turnStirrerOff(self) -> None:
        """
        Stop stirrer.

        :return:
            None
        """
        pass
