import logging
from abc import ABC,abstractmethod
from typing import Any, Optional

from localization import load_translation
from util.logger import MultiprocessingLogger


class TempController(ABC):
    def __init__(self, config: dict[str, Any], devices: dict[str, Any]):
        self._logger: Optional[logging.Logger] = None
        self.device_name = config['id']
        self.t = load_translation()

        # ensure top-level required params
        missing = [k for k in ('maxTemp', 'minTemp') if k not in config]
        if missing:
            raise KeyError(f"Device '{self.device_name}' missing required parameter(s): {', '.join(missing)}")

        # handle optional pidConfig
        pid = config.get('pidConfig')
        if pid is None:
            self.pidConfig = None
        else:
            if not isinstance(pid, dict):
                raise TypeError(
                    f"Device '{self.device_name}' parameter pidConfig has invalid type, "
                    "must be a dict with numeric 'P','I','D'"
                )
    
            # required PID keys
            required_pid = [k for k in ('P', 'I', 'D') if k not in pid]
            if required_pid:
                raise KeyError(
                    f"Device '{self.device_name}' missing required parameter(s) in pidConfig: "
                    f"{', '.join(required_pid)}"
                )
    
            # defaults for the rest
            defaults = {
                'proportionalOnMeasurement': False,
                'differentialOnMeasurement': True,
                'minOutput': -100,
                'maxOutput': 100,
                'dutyCycleLength': 10,
            }
            for key, default in defaults.items():
                pid.setdefault(key, default)
    
            self.pidConfig = pid

    @property
    def logger(self) -> logging.Logger:
        if not self._logger:
            self._logger = MultiprocessingLogger.get_logger(type(self).__name__)
        return self._logger

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
    def getPIDConfig(self) -> dict[str, Any]:
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
