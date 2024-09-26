import hardware.stirring.core as stirrer
import hardware.reagentdispenser.core as rd
import hardware.temperaturecontroller.core as tc
import hardware.thermometer.core as thermometer
import hardware.gpiochip.core as gpiochip
from config import microlabConfig as config
import yaml
from os.path import exists
import logging
from functools import cmp_to_key


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
    controllerHardware = {"devices": []}

    if config.controllerHardware != "custom":
        path = '{0}/{1}.yaml'.format(config.controllerHardwareDirectory, config.controllerHardware)
        if not exists(path):
            raise Exception("No board configuration found for '{0}'".format(config.controllerHardware))
        with open(path) as inf:
            controllerHardware = yaml.safe_load(inf)

    userHardware = {"devices": []}
    lab_hardware_path = '{0}/{1}.yaml'.format(config.labHardwareDirectory, config.labHardware)
    with open(lab_hardware_path) as inf:
        userHardware = yaml.safe_load(inf)

    return {"devices": sort_device_configs(controllerHardware["devices"]) 
                        + sort_device_configs(userHardware["devices"])}


def setupDevices(deviceDefinitions: list[dict]):
    validateConfiguration(deviceDefinitions)
    
    devices = {}

    for device in deviceDefinitions:
        logging.info('Loading device "{0}".'.format(device['id']))
        logging.debug('{0} configuration: {1}'.format(device['id'], device))
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
        else:
            raise Exception("Unsupported device type '{0}'".format(deviceType))
        logging.info('"{0}" loaded successfully.'.format(device['id']))
    return devices


def validateConfiguration(deviceConfigs: list[dict]):
    deviceDict = {}
    sorted_device_configs = sort_device_configs(deviceConfigs)
    for device in sorted_device_configs:
        if deviceDict.get(device['id'], None) is None:
            deviceDict[device['id']] = device
        else:
            raise Exception("Duplicate device id {0}".format(device['id']))
        if device.get('dependencies'):
            for dependency in device["dependencies"]:
                # Given that the device list has been sorted by dependencies,
                # if one of our dependencies is not in the dict of checked
                # devices, there must be a circular dependency.
                if deviceDict.get(dependency, None) is None:
                    raise Exception("Circular dependency detected between devices '{0}' and '{1}'. Device configuration must be acyclic.".format(device['id'], dependency))
    
    return False
