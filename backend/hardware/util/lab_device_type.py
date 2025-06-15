from __future__ import annotations
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    # only for mypy / IDE — won't actually import at runtime
    import hardware.stirring.core as stirrer
    import hardware.reagentdispenser.core as rd
    import hardware.temperaturecontroller.core as tc
    import hardware.thermometer.core as thermometer
    import hardware.gpiochip.core as gpiochip
    import hardware.grbl.core as grbl

LabDevice = Union[
    'tc.TempController',
    'stirrer.Stirrer',
    'rd.ReagentDispenser',
    'thermometer.TempSensor',
    'gpiochip.GPIOChip',
    'grbl.GRBL',
]
