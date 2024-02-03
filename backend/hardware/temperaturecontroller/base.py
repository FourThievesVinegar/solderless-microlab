from abc import ABC,abstractmethod

class TempController(ABC):

    @abstractmethod
    def __init__(self, args, devices):
        if "maxTemp" not in args:
            raise KeyError("Device '{0}' missing required parameter maxTemp".format(args['id']))
        if "minTemp" not in args:
            raise KeyError("Device '{0}' missing required parameter minTemp".format(args['id']))

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

    @abstractmethod
    def getMaxTemperature():
        """
        Read the max allowed temperature of the microlab in celsius

        :return:
        """
        pass

    @abstractmethod
    def getMinTemperature():
        """
        Read the minimum allowed temperature of the microlab in celsius

        :return:
        """
        pass
