from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Optional

from localization import load_translation
from util.logger import MultiprocessingLogger


class LoggerMixin:
    """Provides a .logger property that caches a MultiprocessingLogger."""
    _logger: Optional[logging.Logger] = None

    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            # use the concrete class name as the logger name
            self._logger = MultiprocessingLogger.get_logger(type(self).__name__)
        return self._logger


class LabDevice(ABC, LoggerMixin):
    """
    Abstract base for all lab hardware devices.
    - provides .logger
    - enforces .close()
    """

    def __init__(self, device_name: str):
        self.device_name = device_name
        self.t = load_translation()

    @abstractmethod
    def close(self) -> None:
        """
        Clean up / release any resources (e.g. GPIO lines, file handles).
        """
        pass
