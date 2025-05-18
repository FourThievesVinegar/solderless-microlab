from __future__ import annotations

from hardware.gpiochip.base import LINE_REQ_DIR_OUT, GPIOChip


class GPIODChipSimulation(GPIOChip):
    def __init__(self, gpio_config: dict):
        """
         :param gpio_config: {
            "lineAliases": {alias_str: line_number, …}  # optional
        }
        """
        chip_name = 'simulation'
        pin_aliases = dict(gpio_config.get('lineAliases', {}))
        super().__init__(chip_name, pin_aliases)
        self.logger.debug(f'Configured lineAliases: {pin_aliases!r}')

        self.output_offsets = []
        self.output_values = []
        # self.output_lines = []
        self.chip = None  # no real chip in simulation

    def __output(self):
        """
        Outputs values on every line that has been setup
        """
        pass

    def setup(self, pin: str | int, pinType: str = LINE_REQ_DIR_OUT, value: int = 0) -> None:
        """ :inheritdoc: """
        pin_number = self._get_pin(pin)

        # TODO: add better simulation
        if pinType == LINE_REQ_DIR_OUT:
            self.output_offsets.append(pin_number)
            self.output_values.append(value)
            self.__output()

    def output(self, pin: str | int, value: int) -> None:
        """ :inheritdoc: """
        pin_number = self._get_pin(pin)
        index = self.output_offsets.index(pin_number)
        self.output_values[index] = value
        self.__output()
