from copy import copy
from functools import cmp_to_key
from os import path
from typing import Any

import yaml

import hardware.gpiochip.core as gpiochip
import hardware.grbl.core as grbl
import hardware.reagentdispenser.core as rd
import hardware.stirring.core as stirrer
import hardware.temperaturecontroller.core as tc
import hardware.thermometer.core as thermometer
from config import microlab_config as config
from hardware.lab_device import LabDevice
from localization import load_translation
from util.logger import MultiprocessingLogger


def sort_device_configs(device_configs: list[dict]) -> list[dict]:
    def compare_devices(a: dict, b: dict):
        if b.get('dependencies') and a['id'] in b['dependencies']:
            return -1
        if a.get('dependencies') and b['id'] in a['dependencies']:
            return 1
        if a['id'] < b['id']:
            return -1
        if a['id'] > b['id']:
            return 1
        return 0

    return sorted(device_configs, key=cmp_to_key(compare_devices))


def load_hardware_configuration() -> dict[str, list[dict]]:
    t = load_translation()

    controller_hardware = {'devices': []}
    if config.controllerHardware != 'custom':
        fqfp_controller_config = path.join(config.controllerHardwareDirectory, f'{config.controllerHardware}.yaml')
        if not path.exists(fqfp_controller_config):
            raise FileNotFoundError(t['no-board-config'].format(config.controllerHardware))
        with open(fqfp_controller_config) as inf:
            controller_hardware = yaml.safe_load(inf)

    lab_hardware = {'devices': []}
    fqfp_lab_config = path.join(config.labHardwareDirectory, f'{config.labHardware}.yaml')
    with open(fqfp_lab_config) as inf:
        lab_hardware = yaml.safe_load(inf)

    return {
        'devices': sort_device_configs(controller_hardware['devices']) + sort_device_configs(lab_hardware['devices'])
    }


def setup_devices(device_definitions: list[dict[str, Any]]) -> dict[str, LabDevice]:
    t = load_translation()

    validate_configuration(device_definitions)
    logger = MultiprocessingLogger.get_logger(__name__)

    devices: dict[str, LabDevice] = {}
    for device_config in device_definitions:
        logger.info(t['loading-config'].format(device_config['id']))
        logger.debug(t['config'].format(device_config['id'], device_config))
        device_type = device_config['type']
        device_id = device_config['id']
        if device_type == 'tempController':
            devices[device_id] = tc.create_temperature_controller(device_config, devices)
        elif device_type == 'stirrer':
            devices[device_id] = stirrer.create_stirrer(device_config, devices)
        elif device_type == 'reagentDispenser':
            devices[device_id] = rd.create_reagent_dispenser(device_config, devices)
        elif device_type == 'thermometer':
            devices[device_id] = thermometer.create_thermometer(device_config, devices)
        elif device_type == 'gpiochip':
            devices[device_id] = gpiochip.create_gpio_chip(device_config, devices)
        elif device_type == 'grbl':
            devices[device_id] = grbl.create_grbl(device_config, devices)
        else:
            raise ValueError(t['unsupported-device-type'].format(device_type))
        logger.info(t['loaded-config'].format(device_config['id']))
    return devices


def _check_for_missing_dependency(current_device_config: dict, device_configurations: dict[str, Any]) -> None:
    t = load_translation()

    dependencies = current_device_config.get('dependencies', [])
    for dependency in dependencies:
        if dependency not in device_configurations:
            raise ValueError(t['missing-config'].format(dependency))


def _check_for_cyclical_dependency(
    current_device_id: str, current_device_config: dict, device_configurations: dict[str, Any]
) -> None:
    # We're making a copy as we're going to be altering 'dependencies' to walk the dependency tree
    t = load_translation()

    dependencies = copy(current_device_config.get('dependencies', []))
    for dependency in dependencies:
        if dependency == current_device_id:
            raise ValueError(t['circular-dependency-device-error'].format(current_device_id, dependency))
        child_dependencies = device_configurations[dependency].get('dependencies', [])
        for child_dependency in child_dependencies:
            if child_dependency not in dependencies:
                dependencies.append(child_dependency)


def _check_for_missing_and_circular_hardware_deps(device_configurations: dict[str, Any]) -> None:
    for device_id, device_config in device_configurations.items():
        # Only consider checking dependencies if they are present
        if device_config.get('dependencies'):
            _check_for_missing_dependency(device_config, device_configurations)
            _check_for_cyclical_dependency(device_id, device_config, device_configurations)


def validate_configuration(device_definitions: list[dict[str, Any]]) -> None:
    t = load_translation()

    device_configurations: dict[str, dict[str, Any]] = {}
    for device_config in device_definitions:
        if device_configurations.get(device_config['id'], None) is None:
            device_configurations[device_config['id']] = device_config
        else:
            raise ValueError(t['duplicate-device-id'].format(device_config['id']))
    _check_for_missing_and_circular_hardware_deps(device_configurations)
