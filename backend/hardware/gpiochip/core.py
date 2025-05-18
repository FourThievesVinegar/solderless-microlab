"""
This module contains the implementations for gpio control. See base.py for the abstract class used
and the individual files for configuration information.
"""
from hardware.gpiochip.base import GPIOChip


def createGPIOChip(gpio_config: dict, devices: dict) -> GPIOChip:
    gpio_type = gpio_config['implementation']
    if gpio_type == 'gpiod':
        from hardware.gpiochip.gpiod_chip import GPIODChip
        return GPIODChip(gpio_config)
    if gpio_type == 'simulation':
        from hardware.gpiochip.gpiod_simulation import GPIODChipSimulation
        return GPIODChipSimulation(gpio_config)
    if gpio_type == 'gpiod_chipset':
        from hardware.gpiochip.gpiod_chipset import GPIODChipset
        return GPIODChipset(gpio_config, devices)
    if gpio_type == 'grbl':
        from hardware.gpiochip.grbl_chip import GRBLChip
        return GRBLChip(gpio_config, devices)
    raise ValueError(
        'Unsupported chip: id={config[id]} '
        'type={config[type]} implementation={config[implementation]}'.format(config=gpio_config)
    )
