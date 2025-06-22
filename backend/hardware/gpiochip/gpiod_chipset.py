from __future__ import annotations

from typing import Literal

from hardware.gpiochip.base import GPIOChip, LINE_REQ_DIR_OUT
from hardware.gpiochip.gpiod_chip import GPIODChip
from hardware.lab_device import LabDevice


class GPIODChipset(GPIOChip):
    def __init__(self, gpio_config: dict, devices: dict[str, LabDevice]):
        """
        :param gpio_config: {
            "chipName":    # name of the chip in gpiod
            "defaultChipID":
            "additionalChips": [...],
        }
        :param devices: mapping chip_id -> device instance
        """
        super().__init__(gpio_config['id'], {})

        # build chips dict in one go
        default_id = gpio_config['defaultChipID']
        additional = gpio_config.get('additionalChips', [])
        self.chips: dict[str, GPIODChip] = (
            {default_id: devices[default_id]}
            | {cid: devices[cid] for cid in additional}
        )

        self.line_alias_to_chip: dict[str, str] = dict()
        for chip_id, chip in self.chips.items():
            for alias, line in chip.pin_aliases.items():
                if alias not in self.line_alias_to_chip:
                    self.line_alias_to_chip[alias] = chip_id
                else:
                    self.logger.warning(self.t['chip-conflict'].format(alias, chip_id, self.line_alias_to_chip[alias]))

        self.logger.debug(f'Resolved line aliases: {self.line_alias_to_chip!r}')

    def _get_chip_id(self, pin: str | int) -> str:
        if isinstance(pin, int):
            raise ValueError(f"{self.__class__.__name__}.setup 'pin' argument must must be a string Pin Alias")
        chip_id = self.line_alias_to_chip.get(pin) or 'defaultChip'
        return chip_id

    def setup(self, pin: str | int, pin_type: Literal['input', 'output'] = LINE_REQ_DIR_OUT, value: int = 0) -> None:
        """
        Sets up pin for use, currently only output is supported.

        :param pin:
            The pin to output on. Must be a line alias.
        :param pin_type:
            One of "output" or "input". Currently only "output" is supported
        :param value:
            Either 0 or 1, the value to output on the pin
        :return:
            None
        """
        chip_id = self._get_chip_id(pin)
        return self.chips[chip_id].setup(pin, pin_type, value)

    def output(self, pin: str, value: int) -> None:
        """
        Outputs a new value to specified pin

        :param pin:
            The pin to output on. Must be a line alias.
        :param value:
            Either 0 or 1, the value to output on the pin
        :return:
            None
        """
        chip_id = self._get_chip_id(pin)
        return self.chips[chip_id].output(pin, value)

    def close(self) -> None:
        for chip in self.chips.values():
            chip.close()
