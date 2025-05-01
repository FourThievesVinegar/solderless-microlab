import hardware.stirring.core as stirrer
import hardware.reagentdispenser.core as rd
import hardware.temperaturecontroller.core as tc
import hardware.thermometer.core as thermometer
import hardware.gpiochip.core as gpiochip
import hardware.grbl.core as grbl
from config import microlabConfig as config
import yaml
from os.path import exists
from functools import cmp_to_key
from copy import copy
from util.logger import MultiprocessingLogger
from localization import load_translation

def sort_device_configs(deviceConfigs: list[dict]):
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

    return sorted(deviceConfigs, key=cmp_to_key(compare_devices))


def loadHardwareConfiguration() -> dict:
    t=load_translation()
  
    controllerHardware = {"devices": []}

    if config.controllerHardware != "custom":
        path = '{0}/{1}.yaml'.format(config.controllerHardwareDirectory, config.controllerHardware)
        if not exists(path):
            raise Exception(t['no-board-config'].format(config.controllerHardware))
        with open(path) as inf:
            controllerHardware = yaml.safe_load(inf)

    userHardware = {"devices": []}
    lab_hardware_path = '{0}/{1}.yaml'.format(config.labHardwareDirectory, config.labHardware)
    with open(lab_hardware_path) as inf:
        userHardware = yaml.safe_load(inf)

    return {"devices": sort_device_configs(controllerHardware["devices"]) 
                        + sort_device_configs(userHardware["devices"])}


def setupDevices(deviceDefinitions: list[dict]):
    t=load_translation()
  
    validateConfiguration(deviceDefinitions)
    logger = MultiprocessingLogger.get_logger(__name__)
    
    devices = {}

    for device in deviceDefinitions:
        logger.info(t['loading-config'].format(device['id']))
        logger.debug(t['config'].format(device['id'], device))
        deviceType = device["type"]
        deviceID = device['id']
        if deviceType == "tempController":
            devices[deviceID] = tc.createTemperatureController(device, devices)
        elif deviceType == "stirrer":
            devices[deviceID] = stirrer.createStirrer(device, devices)
        elif deviceType == "reagentDispenser":
            devices[deviceID] = rd.createReagentDispenser(device, devices)
        elif deviceType == "thermometer":
            devices[deviceID] = thermometer.createThermometer(device, devices)
        elif deviceType == "gpiochip":
            devices[deviceID] = gpiochip.createGPIOChip(device, devices)
        elif deviceType == "grbl":
            devices[deviceID] = grbl.createGRBL(device, devices)
        else:
            raise Exception(t['unsupported-device-type'].format(deviceType))
        logger.info(t['loaded-config'].format(device['id']))
    return devices


def _checkForMissingDependency(current_device_config: dict, allDeviceData: dict):
    t=load_translation()
    
    dependencies = current_device_config.get('dependencies', [])
    for dependency in dependencies:
        if dependency not in allDeviceData:
            raise Exception(t['missing-config'].format(dependency))


def _checkForCyclicalDependency(current_device_id: str, current_device_config: dict, allDeviceData: dict):
    # We're making a copy as we're going to be altering 'dependencies' to walk the dependency tree
    t=load_translation()
    
    dependencies = copy(current_device_config.get('dependencies', []))
    for dependency in dependencies:
        if dependency == current_device_id:
            raise Exception(t['circular-dependency-device-error'].format(current_device_id, dependency))
        child_dependencies = allDeviceData[dependency].get('dependencies', [])
        for child_dependency in child_dependencies:
            if child_dependency not in dependencies:
                dependencies.append(child_dependency)


def _checkForMissingAndCircularHardwareDeps(deviceData: dict):
    for device_id, device_config in deviceData.items():
        # We only care about checking deps if they are present
        if device_config.get('dependencies'):
            _checkForMissingDependency(device_config, deviceData)
            _checkForCyclicalDependency(device_id, device_config, deviceData)


def validateConfiguration(deviceConfigs: list[dict]):
    t=load_translation()
  
    deviceDict = {}
    for device in deviceConfigs:
        if deviceDict.get(device['id'], None) is None:
            deviceDict[device['id']] = device
        else:
            raise Exception(t['duplicate-device-id'].format(device['id']))
    _checkForMissingAndCircularHardwareDeps(deviceDict)
    
    return False
