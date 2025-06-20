from abc import abstractmethod

from hardware.lab_device import LabDevice
from localization import load_translation


class TempSensor(LabDevice):
    def __init__(self, device_name: str):
        super().__init__(device_name)
        self.t = load_translation()

    @abstractmethod
    def get_temp(self) -> float:
        """
        Get the temperature of the sensor in Celsius.
        :return:
            Temperature in Celsius
        """
        pass
