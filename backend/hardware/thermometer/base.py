from abc import abstractmethod

from hardware.lab_device import LabDevice


class TempSensor(LabDevice):
    def __init__(self, device_name: str):
        super().__init__(device_name)

    @abstractmethod
    def get_temp(self) -> float:
        """
        Get the temperature of the sensor in Celsius.
        :return:
            Temperature in Celsius
        """
        pass
