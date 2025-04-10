from abc import ABC,abstractmethod
from localization import load_translation


class TempController(ABC):

    @abstractmethod
    def __init__(self, args, devices):
        t=load_translation()
        
        if "maxTemp" not in args:
            raise KeyError(t['device-miss-max-temp'].format(args['id']))
        if "minTemp" not in args:
            raise KeyError(t['device-miss-min-temp'].format(args['id']))
        if "pidConfig" in args:
            pidConfig = args["pidConfig"]
            if not isinstance(pidConfig, dict):
                raise TypeError(t['pid-config-error'].format(args['id']))
            if "P" not in pidConfig:
                raise KeyError(t['pid-config-miss-p'].format(args['id']))
            if "I" not in pidConfig:
                raise KeyError(t['pid-config-miss-i'].format(args['id']))
            if "D" not in pidConfig:
                raise KeyError(t['pid-config-miss-d'].format(args['id']))
            
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
            proportionalOnMeasurement: Boolean 
            differentialOnMeasurement: Boolean 
            minOutput: number
            maxOutput: number
            dutyCycleLength: number
        """
        return self.pidConfig
