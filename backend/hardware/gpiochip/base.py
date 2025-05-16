from __future__ import annotations

from abc import ABC, abstractmethod

from jinja2.nodes import Literal

from util.logger import MultiprocessingLogger

LINE_REQ_DIR_OUT = 'output'
LINE_REQ_DIR_IN = 'input'


class GPIOChip(ABC):
    def __init__(self, logger_tag: str, chip_name: str, pin_aliases: dict[str, int]):
        self.logger = MultiprocessingLogger.get_logger(logger_tag)
        self.chip_name = chip_name
        self.pin_aliases = pin_aliases

    def _get_pin(self, pin: str | int) -> int:
        """
        Converts string aliases to the corresponding line number.
        Raises ValueError if pin is a non-existent alias.
        :param pin: alias (str) or direct line number (int)
        :return: the line number for that pin
        """
        if isinstance(pin, str):
            alias = self.pin_aliases.get(pin)
            if alias is None:
                raise ValueError(f'Invalid GPIO pin {pin}')
            return alias
        return pin

    @abstractmethod
    def setup(self, pin: str | int, pinType: Literal['input', 'output'], value: int) -> None:
        """
        Sets up pin for use, currently only output is supported.

        :param pin:
            The pin to setup. Either a defined alias or the line number for the pin
        :param pinType:
            One of "output" or "input". Currently only "output" is supported
        :param value:
            Either 0 or 1, the value to output on the pin
        :return:
            None
        """
        pass

    @abstractmethod
    def output(self, pin: str | int, value: int) -> None:
        """
        Outputs a new value to specified pin

        :param pin:
            The pin to output on. Either a defined alias or the line number for the pin
        :param value:
            Either 0 or 1, the value to output on the pin
        :return:
            None
        """
        pass
