from abc import ABC,abstractmethod

class TempController(ABC):
    @abstractmethod
    def turnHeaterOn():
        """
        Turns the heater on.

        :return:
        None
        """
        pass


    @abstractmethod
    def turnHeaterOff():
        """
        Turns the heater off.

        :return:
        None
        """
        pass

    @abstractmethod
    def turnCoolerOn():
        """
        Turns the cooler on.

        :return:
        None
        """
        pass

    @abstractmethod
    def turnCoolerOff():
        """
        Turns the cooler off.

        :return:
        None
        """
        pass

    @abstractmethod
    def getTemp():
        """
        Reads the temperature of the microlab

        :return:
        """
        pass
