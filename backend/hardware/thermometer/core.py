"""
This module contains the implementations of the Thermometer. See base.py for the abstract class used
and either the individual files or backend/config.py for configuration information.
"""
from typing import Any

from hardware.thermometer.base import TempSensor
from hardware.lab_device import LabDevice


def create_thermometer(device_config: dict[str, Any], devices: dict[str, LabDevice]) -> TempSensor:
    thermometer_type = device_config['implementation']
    if thermometer_type == 'w1_therm':
        from hardware.thermometer.w1_therm import W1TempSensor
        return W1TempSensor()
    elif thermometer_type == 'serial':
        from hardware.thermometer.serial import SerialTempSensor
        return SerialTempSensor(device_config)
    elif thermometer_type == 'simulation':
        from hardware.thermometer.serial_simulation import SerialTempSensorSimulation
        return SerialTempSensorSimulation(device_config)
    raise ValueError(
        'Unsupported device: id={config[id]} '
        'type={config[type]} implementation={config[implementation]}'.format(config=device_config)
    )
