import hardware.stirring.core as stirrer
import hardware.reagentdispenser.core as rd
import hardware.temperaturecontroller.core as tc
import hardware.thermometer.core as thermometer
import hardware.gpiochip.core as gpiochip
from config import microlabConfig as config
import yaml
from os.path import exists
import logging


def loadHardwareConfiguration() -> dict:
    if config.controllerHardware != "custom":
        path = '{0}/{1}.yaml'.format(config.controllerHardwareDirectory, config.controllerHardware)
        if not exists(path):
            raise Exception("No board configuration found for '{0}'".format(config.controllerHardware))
        controllerHardware = yaml.safe_load(open(path, 'r'))
    else:
        controllerHardware = {"devices": []}

    userHardware = yaml.safe_load(
        open('{0}/{1}.yaml'.format(config.labHardwareDirectory, config.labHardware), 'r'))

    return {"devices": controllerHardware["devices"] + userHardware["devices"]}


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
    for device in deviceConfigs:

        if deviceDict.get(device['id'], None) is None:
            deviceDict[device['id']] = device
        else:
            raise Exception("Duplicate device id {0}".format(device['id']))
    
    return False
