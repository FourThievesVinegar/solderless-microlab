from abc import abstractmethod

from hardware.lab_device import LabDevice


class Stirrer(LabDevice):
    def __init__(self, device_name: str) -> None:
        super().__init__(device_name)

    @abstractmethod
    def turn_stirrer_on(self) -> None:
        """
        Start stirrer.

        :return:
            None
        """
        pass

    @abstractmethod
    def turn_stirrer_off(self) -> None:
        """
        Stop stirrer.

        :return:
            None
        """
        pass
