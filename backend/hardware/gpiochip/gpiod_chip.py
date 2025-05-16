from __future__ import annotations

from typing import Literal

import gpiod

from hardware.gpiochip.base import GPIOChip, LINE_REQ_DIR_OUT


class GPIODChip(GPIOChip):
    def __init__(self, gpio_config: dict):
        """
        Constructor. Initializes the GPIO chip.
        :param gpio_config:
          dict
            chipName
              Name of the chip according to gpiod
            lineAliases
              dictionary mapping strings to line numbers
              for adding human readable names to GPIO lines
        """
        self.output_offsets = []
        self.output_values = []
        self.output_lines = []

        chip_name = gpio_config['chipName']
        self.chip = gpiod.Chip(chip_name)

        # copy any provided aliases, or use empty dict
        pin_aliases = dict(gpio_config.get('lineAliases', {}))
        super().__init__(__name__, chip_name, pin_aliases)
        self.logger.debug(f'Configured lineAliases: {pin_aliases!r}')

    def __output(self):
        """
        Outputs values on every line that has been setup
        """
        lines = self.chip.get_lines(self.output_offsets)
        lines.request(consumer='microlab', type=gpiod.LINE_REQ_DIR_OUT)
        lines.set_values(self.output_values)
        lines.release()

    def setup(self, pin: str | int, pinType: Literal['input', 'output'] = LINE_REQ_DIR_OUT, value: int = 0) -> None:
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
        pin_number = self._get_pin(pin)
        
        if pinType == LINE_REQ_DIR_OUT:
            # line = self.chip.get_line(pin_number)
            # line.request(consumer="microlab", type=gpiod.LINE_REQ_DIR_OUT)
            self.output_offsets.append(pin_number)
            self.output_values.append(value)
            # self.output_lines.append(line)
            self.__output()

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
        pin_number = self._get_pin(pin)
        index = self.output_offsets.index(pin_number)
        self.output_values[index] = value
        self.__output()
