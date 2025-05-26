import logging
from abc import ABC, abstractmethod
from typing import Optional, Any

from localization import load_translation
from util.logger import MultiprocessingLogger


class TempSensor(ABC):
    def __init__(self, device_name: str):
        self._logger: Optional[logging.Logger] = None
        self.device_name = device_name
        self.t = load_translation()

    @property
    def logger(self) -> logging.Logger:
        if not self._logger:
            self._logger = MultiprocessingLogger.get_logger(type(self).__name__)
        return self._logger

    @abstractmethod
    def getTemp(self) -> float:
        """
        Get the temperature of the sensor in Celsius.
        :return:
            Temperature in Celsius
        """
        pass
