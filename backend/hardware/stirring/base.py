import logging
from abc import ABC, abstractmethod
from typing import Optional

from localization import load_translation
from util.logger import MultiprocessingLogger


class Stirrer(ABC):
    def __init__(self, device_name: str) -> None:
        self._logger: Optional[logging.Logger] = None
        self.device_name = device_name
        self.t = load_translation()

    @property
    def logger(self) -> logging.Logger:
        if not self._logger:
            self._logger = MultiprocessingLogger.get_logger(type(self).__name__)
        return self._logger

    @abstractmethod
    def turnStirrerOn(self) -> None:
        """
        Start stirrer.

        :return:
            None
        """
        pass

    @abstractmethod
    def turnStirrerOff(self) -> None:
        """
        Stop stirrer.

        :return:
            None
        """
        pass
