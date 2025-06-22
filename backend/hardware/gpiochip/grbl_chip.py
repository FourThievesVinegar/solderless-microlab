from __future__ import annotations

from typing import Literal

from hardware.gpiochip.base import GPIOChip, LINE_REQ_DIR_OUT
from hardware.lab_device import LabDevice


class GRBLChip(GPIOChip):
    def __init__(self, gpio_config: dict, devices: dict[str, LabDevice]):
        """
        Constructor. Initializes the GPIO chip.
        :param gpio_config:
          dict
            grblID
              ID of the grbl device
            lineAliases
              dictionary mapping strings to pin numbers
              for adding human-readable names to GPIO pins
        """
        pin_aliases = dict(gpio_config.get('lineAliases', {}))
        super().__init__(gpio_config['id'], pin_aliases)
        self.logger.debug(f'Configured lineAliases: {pin_aliases!r}')

        self.output_offsets = []
        self.output_values = []
        self.device: 'hardware.grbl.base.GRBL' = devices[gpio_config['grblID']]

    def __output(self) -> None:
        """
        Outputs values on every pin that has been setup
        """
        for (val, pin) in (zip(self.output_values, self.output_offsets)):
            if val == 0:
                # M65: Disable (turn off) the digital output for the specified pin
                command = 'M65'
            else:
                # M64: Enable (turn on) the digital output for the specified pin
                command = 'M64'

            self.device.write_gcode(f'{command} P{pin}')

    def setup(self, pin: str | int, pin_type: Literal['input', 'output'] = LINE_REQ_DIR_OUT, value: int = 0) -> None:
        """ :inheritdoc: """
        pin_number = self._get_pin(pin)

        if pin_type == LINE_REQ_DIR_OUT:
            self.output_offsets.append(pin_number)
            self.output_values.append(value)
            self.__output()

    def output(self, pin: str | int, value: int) -> None:
        """ :inheritdoc: """
        pin_number = self._get_pin(pin)
        index = self.output_offsets.index(pin_number)
        self.output_values[index] = value
        self.__output()

    def close(self) -> None:
        self.device.close()
