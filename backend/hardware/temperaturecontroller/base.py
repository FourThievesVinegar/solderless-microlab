from abc import ABC,abstractmethod

class TempController(ABC):
    @abstractmethod
    def turnHeaterOn():
        """
        Sets the heater flag for the simulation.

        :return:
        None
        """
        pass


    @abstractmethod
    def turnHeaterOff():
        """
        Un-sets the heater flag for the simulation.

        :return:
        None
        """
        pass

    @abstractmethod
    def turnCoolerOn():
        """
        Sets the cooler flag for the simulation.

        :return:
        None
        """
        pass

    @abstractmethod
    def turnCoolerOff():
        """
        Un-sets the heater flag for the simulation.

        :return:
        None
        """
        pass

    @abstractmethod
    def getTemp():
        """
        Simulates and returns temperature.

        Temperature starts off at 24C and changes every time the function is called as follows:
            heater flag on: +1C
            heater flag off: -0.1C
        :return:
        """
        pass
