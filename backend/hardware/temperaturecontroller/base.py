from abc import ABC,abstractmethod


class TempController(ABC):

    @abstractmethod
    def __init__(self, args, devices):
        if "maxTemp" not in args:
            raise KeyError("Device '{0}' missing required parameter maxTemp".format(args['id']))
        if "minTemp" not in args:
            raise KeyError("Device '{0}' missing required parameter minTemp".format(args['id']))
        if "pidConfig" in args:
            pidConfig = args["pidConfig"]
            if not isinstance(pidConfig, dict):
                raise TypeError("Device '{0}' parameter pidConfig has invalid type, must be a dictionary containing numeric values for 'P','I', and 'D'.".format(args['id']))
            if "P" not in pidConfig:
                raise KeyError("Device '{0}' missing required parameter 'P' in pidConfig".format(args['id']))
            if "I" not in pidConfig:
                raise KeyError("Device '{0}' missing required parameter 'I' in pidConfig".format(args['id']))
            if "D" not in pidConfig:
                raise KeyError("Device '{0}' missing required parameter 'D' in pidConfig".format(args['id']))
            
            if "proportionalOnMeasurement" not in pidConfig:
                pidConfig["proportionalOnMeasurement"] = False
            if "differentialOnMeasurement" not in pidConfig:
                pidConfig["differentialOnMeasurement"] = True
            if "minOutput" not in pidConfig:
                pidConfig["minOutput"] = -100
            if "maxOutput" not in pidConfig:
                pidConfig["maxOutput"] = 100
            if "dutyCycleLength" not in pidConfig:
                pidConfig["dutyCycleLength"] = 10

            self.pidConfig = args["pidConfig"]
        else:
            self.pidConfig = None

    @abstractmethod
    def turnHeaterOn(self) -> None:
        """
        Turns the heater on.

        :return:
        None
        """
        pass

    @abstractmethod
    def turnHeaterOff(self) -> None:
        """
        Turns the heater off.

        :return:
        None
        """
        pass

    @abstractmethod
    def turnHeaterPumpOn(self) -> None:
        """
        Turns the heater pump on.

        :return:
        None
        """
        pass

    @abstractmethod
    def turnHeaterPumpOff(self) -> None:
        """
        Turns the heater pump off.

        :return:
        None
        """
        pass

    @abstractmethod
    def turnCoolerOn(self) -> None:
        """
        Turns the cooler on.

        :return:
        None
        """
        pass

    @abstractmethod
    def turnCoolerOff(self) -> None:
        """
        Turns the cooler off.

        :return:
        None
        """
        pass

    @abstractmethod
    def getTemp(self) -> float:
        """
        Reads the temperature of the microlab

        :return:
        """
        pass

    @abstractmethod
    def getMaxTemperature(self) -> float:
        """
        Read the max allowed temperature of the microlab in Celsius

        :return:
        """
        pass

    @abstractmethod
    def getMinTemperature(self) -> float:
        """
        Read the minimum allowed temperature of the microlab in Celsius

        :return:
        """
        pass

    @abstractmethod
    def getPIDConfig(self) -> dict:
        """
        Read the temperature controller PID configuration

        :return:
        None if not configured, otherwise:
        object
            P: number
            I: number
            D: number
            proportionalOnMeasurement: Boolean 
            differentialOnMeasurement: Boolean 
            minOutput: number
            maxOutput: number
            dutyCycleLength: number
        """
        return self.pidConfig
