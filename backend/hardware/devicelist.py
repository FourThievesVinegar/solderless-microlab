from typing import Any

import hardware.stirring.core as stirrer
import hardware.reagentdispenser.core as rd
import hardware.temperaturecontroller.core as tc
import hardware.thermometer.core as thermometer
import hardware.gpiochip.core as gpiochip
import hardware.grbl.core as grbl
from config import microlab_config as config
import yaml
from os import path
from functools import cmp_to_key
from copy import copy
from util.logger import MultiprocessingLogger
from localization import load_translation


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


def loadHardwareConfiguration() -> dict:
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


def setupDevices(deviceDefinitions: list[dict]) -> dict:
    t = load_translation()

    validateConfiguration(deviceDefinitions)
    logger = MultiprocessingLogger.get_logger(__name__)

    devices: dict[str, Any] = {}

    for device in deviceDefinitions:
        logger.info(t['loading-config'].format(device['id']))
        logger.debug(t['config'].format(device['id'], device))
        device_type = device['type']
        device_id = device['id']
        if device_type == 'tempController':
            devices[device_id] = tc.createTemperatureController(device, devices)
        elif device_type == 'stirrer':
            devices[device_id] = stirrer.createStirrer(device, devices)
        elif device_type == 'reagentDispenser':
            devices[device_id] = rd.createReagentDispenser(device, devices)
        elif device_type == 'thermometer':
            devices[device_id] = thermometer.createThermometer(device, devices)
        elif device_type == 'gpiochip':
            devices[device_id] = gpiochip.createGPIOChip(device, devices)
        elif device_type == 'grbl':
            devices[device_id] = grbl.createGRBL(device, devices)
        else:
            raise ValueError(t['unsupported-device-type'].format(device_type))
        logger.info(t['loaded-config'].format(device['id']))
    return devices


def _checkForMissingDependency(current_device_config: dict, allDeviceData: dict) -> None:
    t = load_translation()

    dependencies = current_device_config.get('dependencies', [])
    for dependency in dependencies:
        if dependency not in allDeviceData:
            raise ValueError(t['missing-config'].format(dependency))


def _checkForCyclicalDependency(current_device_id: str, current_device_config: dict, allDeviceData: dict) -> None:
    # We're making a copy as we're going to be altering 'dependencies' to walk the dependency tree
    t = load_translation()

    dependencies = copy(current_device_config.get('dependencies', []))
    for dependency in dependencies:
        if dependency == current_device_id:
            raise ValueError(t['circular-dependency-device-error'].format(current_device_id, dependency))
        child_dependencies = allDeviceData[dependency].get('dependencies', [])
        for child_dependency in child_dependencies:
            if child_dependency not in dependencies:
                dependencies.append(child_dependency)


def _checkForMissingAndCircularHardwareDeps(devices: dict) -> None:
    for device_id, device_config in devices.items():
        # We only care about checking dependencies if they are present
        if device_config.get('dependencies'):
            _checkForMissingDependency(device_config, devices)
            _checkForCyclicalDependency(device_id, device_config, devices)


def validateConfiguration(deviceConfigs: list[dict]) -> None:
    t = load_translation()

    devices: dict[str, Any] = {}
    for device in deviceConfigs:
        if devices.get(device['id'], None) is None:
            devices[device['id']] = device
        else:
            raise ValueError(t['duplicate-device-id'].format(device['id']))
    _checkForMissingAndCircularHardwareDeps(devices)
