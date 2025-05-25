from __future__ import annotations

from typing import Literal, Optional

import gpiod
from gpiod.line import Direction, Value
from gpiod.line_settings import LineSettings
from gpiod.line_request import LineRequest

from hardware.gpiochip.base import GPIOChip, LINE_REQ_DIR_OUT


class GPIODChip(GPIOChip):
    def __init__(self, gpio_config: dict):
        """
        Initializes the GPIO chip configuration.

        :param gpio_config: dict with keys:
            - chipName: device path for the gpiochip (e.g., '/dev/gpiochip0')
            - lineAliases: optional dict mapping alias strings to line numbers
              for adding human-readable names to GPIO lines
        """
        pin_aliases = dict(gpio_config.get('lineAliases', {}))
        super().__init__(gpio_config['chipName'], pin_aliases)
        self.logger.debug(f'Configured lineAliases: {pin_aliases!r}')

        # track requested offsets and initial values
        self.output_offsets: list[int] = []
        self.output_values: dict[int, Value] = {}

        # create a persistent Chip/LineRequest
        self.device = gpiod.Chip(self.device_name)
        self.request: Optional[LineRequest] = None

    def close(self) -> None:
        """ Explicitly release the LineRequest if it exists. """
        if getattr(self, 'request', None):
            try:
                self.request.release()
            except Exception as e:
                self.logger.warning(f'Error releasing GPIO lines: {e!r}')
            finally:
                self.request = None

    def __del__(self):
        # Python may call this at interpreter shutdown, so keep it defensive.
        try:
            self.close()
        except Exception:
            pass

    def setup(self, pin: str | int, pinType: Literal['input', 'output'] = LINE_REQ_DIR_OUT, value: int = 0) -> None:
        """ :inheritdoc: """
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
            self.request = self.device.request_lines(
                config=settings,
                consumer='microlab'
            )

    def output(self, pin: str | int, value: int):
        """ :inheritdoc: """
        offset = self._get_pin(pin)
        if offset not in self.output_offsets:
            raise ValueError(f'Pin {pin!r} not set up for output')

        # update our cache
        self.output_values[offset] = Value.ACTIVE if value else Value.INACTIVE

        # apply just this line
        self.request.set_values({offset: self.output_values[offset]})
