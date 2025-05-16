from __future__ import annotations

from typing import Literal

from hardware.gpiochip.base import GPIOChip
from hardware.gpiochip.gpiod_chip import GPIODChip
from localization import load_translation
from util.logger import MultiprocessingLogger


class GPIODChipset(GPIOChip):
    def __init__(self, gpio_config: dict, devices: dict):
        """
        :param gpio_config: {
            "chipName":    # name of the chip in gpiod
            "defaultChipID":
            "additionalChips": [...],
        }
        :param devices: mapping chip_id -> device instance
        """
        t = load_translation()

        chipset_name = gpio_config['id']
        super().__init__(__name__, chipset_name, {})

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
                    self.logger.warning(t['chip-conflict'].format(alias, chip_id, self.line_alias_to_chip[alias]))

        self.logger.debug(f'Resolved line aliases: {self.line_alias_to_chip!r}')

    def setup(self, pin: str, pinType: Literal['input', 'output'], value: int) -> None:
        """
        Sets up pin for use, currently only output is supported.

        :param pin:
            The pin to output on. Must be a line alias.
        :param pinType:
            One of "output" or "input". Currently only "output" is supported
        :param value:
            Either 0 or 1, the value to output on the pin
        :return:
            None
        """
        if isinstance(pin, int):
            raise ValueError(f"{self.__class__.__name__}.setup 'pin' argument must must be a string Pin Alias")
        chip_id = self.line_alias_to_chip.get(pin) or 'defaultChip'
        return self.chips[chip_id].setup(pin, pinType, value)

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
        if isinstance(pin, int):
            raise ValueError(f"{self.__class__.__name__}.output 'pin' argument must must be a string Pin Alias")
        chip_id = self.line_alias_to_chip.get(pin) or 'defaultChip'
        return self.chips[chip_id].output(pin, value)
