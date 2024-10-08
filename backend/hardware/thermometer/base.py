from abc import ABC, abstractmethod


class TempSensor(ABC):
    @abstractmethod
    def getTemp(self):
        """
        Get the temperature of the sensor in celsius.
        :return:
            Temperature in Celsius
        """
        pass
