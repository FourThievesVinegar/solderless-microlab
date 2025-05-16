from __future__ import annotations

from hardware.gpiochip.base import LINE_REQ_DIR_OUT, GPIOChip


class GPIODChipSimulation(GPIOChip):
    def __init__(self, gpio_config: dict):
        """
         :param gpio_config: {
            "chipName":    # name of the chip according to gpiod
            "lineAliases": {alias_str: line_number, …}  # optional
        }
        """
        self.output_offsets = []
        self.output_values = []
        self.output_lines = []

        # no real chip in simulation
        chip_name = 'simulation'
        self.chip = None

        # copy any provided aliases, or use empty dict
        pin_aliases = dict(gpio_config.get('lineAliases', {}))
        super().__init__(__name__, chip_name, pin_aliases)
        self.logger.debug(f'Configured lineAliases: {pin_aliases!r}')

    def __output(self):
        """
        Outputs values on every line that has been setup
        """
        pass

    def setup(self, pin: str | int, pinType: str = LINE_REQ_DIR_OUT, value: int = 0) -> None:
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

        # TODO: add better simulation
        if pinType == LINE_REQ_DIR_OUT:
            self.output_offsets.append(pin_number)
            self.output_values.append(value)
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
