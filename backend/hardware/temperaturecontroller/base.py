from abc import abstractmethod
from typing import Any

from hardware.lab_device import LabDevice


class TempController(LabDevice):
    def __init__(self, config: dict[str, Any], devices: dict[str, LabDevice] = None):
        super().__init__(config.get('id', 'TempController'))

        # ensure top-level required params
        missing = [k for k in ('maxTemp', 'minTemp') if k not in config]
        if missing:
            raise KeyError(f"Device '{self.device_name}' missing required parameter(s): {', '.join(missing)}")

        # handle optional pidConfig
        pid_configuration = config.get('pidConfig')
        if pid_configuration is None:
            self.pid_config = None
        else:
            if not isinstance(pid_configuration, dict):
                raise TypeError(
                    f"Device '{self.device_name}' parameter pidConfig has invalid type, "
                    "must be a dict with numeric 'P','I','D'"
                )
    
            # required PID keys
            required_pid = [k for k in ('P', 'I', 'D') if k not in pid_configuration]
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
                pid_configuration.setdefault(key, default)
    
            self.pid_config = pid_configuration

    @abstractmethod
    def turn_heater_on(self) -> None:
        """
        Turns the heater on.

        :return:
        None
        """
        pass

    @abstractmethod
    def turn_heater_off(self) -> None:
        """
        Turns the heater off.

        :return:
        None
        """
        pass

    @abstractmethod
    def turn_heater_pump_on(self) -> None:
        """
        Turns the heater pump on.

        :return:
        None
        """
        pass

    @abstractmethod
    def turn_heater_pump_off(self) -> None:
        """
        Turns the heater pump off.

        :return:
        None
        """
        pass

    @abstractmethod
    def turn_cooler_on(self) -> None:
        """
        Turns the cooler on.

        :return:
        None
        """
        pass

    @abstractmethod
    def turn_cooler_off(self) -> None:
        """
        Turns the cooler off.

        :return:
        None
        """
        pass

    @abstractmethod
    def get_temp(self) -> float:
        """
        Reads the temperature of the microlab in Celsius

        :return:
        """
        pass

    @abstractmethod
    def get_max_temperature(self) -> float:
        """
        Read the max allowed temperature of the microlab in Celsius

        :return:
        """
        pass

    @abstractmethod
    def get_min_temperature(self) -> float:
        """
        Read the minimum allowed temperature of the microlab in Celsius

        :return:
        """
        pass

    @abstractmethod
    def get_pid_config(self) -> dict[str, Any]:
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
        return self.pid_config
