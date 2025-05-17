from __future__ import annotations

from typing import Literal

import gpiod
from gpiod.line import Direction, Value
from gpiod.line_settings import LineSettings

from hardware.gpiochip.base import GPIOChip


class GPIODChip(GPIOChip):
    def __init__(self, gpio_config: dict):
        """
        Initializes the GPIO chip configuration.

        :param gpio_config: dict with keys:
            - chipName: device path for the gpiochip (e.g., '/dev/gpiochip0')
            - lineAliases: optional dict mapping alias strings to line numbers
              for adding human-readable names to GPIO lines
        """
        chip_name = gpio_config['chipName']
        pin_aliases = dict(gpio_config.get('lineAliases', {}))
        super().__init__(chip_name, pin_aliases)
        self.logger.debug(f'Configured lineAliases: {pin_aliases!r}')

        # track requested offsets and initial values
        self.output_offsets: list[int] = []
        self.output_values: dict[int, Value] = {}

        # create a persistent Chip/LineRequest
        self.chip = gpiod.Chip(self.chip_name)
        self.request = None  # type: ignore[assignment]

    def setup(self, pin: str | int, pinType: Literal['input', 'output'] = 'output', value: int = 0):
        offset = self._get_pin(pin)

        if pinType == 'output':
            # record new output
            self.output_offsets.append(offset)
            self.output_values[offset] = Value.ACTIVE if value else Value.INACTIVE

            # build settings for all outputs
            settings = {
                off: LineSettings(
                    direction=Direction.OUTPUT,
                    output_value=self.output_values[off]
                )
                for off in self.output_offsets
            }

            # replace (or create) the LineRequest
            if self.request:
                self.request.release()
            self.request = self.chip.request_lines(
                config=settings,
                consumer='microlab'
            )

    def output(self, pin: str | int, value: int):
        offset = self._get_pin(pin)
        if offset not in self.output_offsets:
            raise ValueError(f'Pin {pin!r} not set up for output')

        # update our cache
        self.output_values[offset] = Value.ACTIVE if value else Value.INACTIVE

        # apply just this line
        self.request.set_values({offset: self.output_values[offset]})
