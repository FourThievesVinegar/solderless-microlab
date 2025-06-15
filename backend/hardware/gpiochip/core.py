"""
This module contains the implementations for gpio control. See base.py for the abstract class used
and the individual files for configuration information.
"""
from typing import Any

from hardware.gpiochip.base import GPIOChip
from hardware.util.lab_device_type import LabDevice


def create_gpio_chip(device_config: dict[str, Any], devices: dict[str, LabDevice]) -> GPIOChip:
    gpio_type = device_config['implementation']
    if gpio_type == 'gpiod':
        from hardware.gpiochip.gpiod_chip import GPIODChip
        return GPIODChip(device_config)
    if gpio_type == 'simulation':
        from hardware.gpiochip.gpiod_simulation import GPIODChipSimulation
        return GPIODChipSimulation(device_config)
    if gpio_type == 'gpiod_chipset':
        from hardware.gpiochip.gpiod_chipset import GPIODChipset
        return GPIODChipset(device_config, devices)
    if gpio_type == 'grbl':
        from hardware.gpiochip.grbl_chip import GRBLChip
        return GRBLChip(device_config, devices)
    raise ValueError(
        'Unsupported device: id={config[id]} '
        'type={config[type]} implementation={config[implementation]}'.format(config=device_config)
    )
