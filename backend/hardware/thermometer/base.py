from abc import ABC, abstractmethod


class TempSensor(ABC):
    @abstractmethod
    def getTemp(self) -> float:
        """
        Get the temperature of the sensor in Celsius.
        :return:
            Temperature in Celsius
        """
        pass
