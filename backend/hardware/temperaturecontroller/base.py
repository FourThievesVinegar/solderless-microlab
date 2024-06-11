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
    def turnHeaterPumpOn():
        """
        Turns the heater pump on.

        :return:
        None
        """
        pass


    @abstractmethod
    def turnHeaterPumpOff():
        """
        Turns the heater pump off.

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

    @abstractmethod
    def getPIDConfig():
        """
        Read the temperature controller PID configuration

        :return:
        None if not configured, otherwise:
        object
            P: number
            I: number
            D: number
            proportionalOnMeasurement: Boolean (optional)
            differentialOnMeasurement: Boolean (optional)
        """
        return None