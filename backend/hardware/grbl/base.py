import logging
from abc import ABC, abstractmethod
from typing import Optional

from util.logger import MultiprocessingLogger


class GRBL(ABC):
    def __init__(self, chip_name: str):
        self._logger: Optional[logging.Logger] = None
        self.chip_name = chip_name

    @property
    def logger(self) -> logging.Logger:
        if not self._logger:
            self._logger = MultiprocessingLogger.get_logger(type(self).__name__)
        return self._logger

    @abstractmethod
    def grblWrite(self, command: str, retries: int = 3) -> None:
        """
        Writes the gcode command to grbl

        :param command:
            The raw gcode command string.
        :param retries:
            Number of times to retry the command should it fail.
            default is 3
        :return:
            None
        """
        pass
