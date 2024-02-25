import hardware.stirring as stirrer
import hardware.reagentdispenser as rd
import hardware.temperaturecontroller as tc
import hardware.thermometer as thermometer
import hardware.gpiochip as gpiochip
from config import microlabConfig as config
import yaml
from os.path import exists

def loadHardwareConfiguration():
  if config.controllerHardware != "custom":
    path = '{0}/{1}.yaml'.format(config.controllerHardwareDirectory, config.controllerHardware)
    if not exists(path):
      raise Exception("No board configuration found for '{0}'".format(config.controllerHardware))
    controllerHardware = yaml.safe_load(open(path, 'r'))
  else:
    controllerHardware = {"devices": []}


  userHardware = yaml.safe_load(open('{0}/{1}.yaml'
            .format(config.labHardwareDirectory, config.labHardware), 'r'))

  return { "devices": controllerHardware["devices"] + userHardware["devices"]}


def setupDevices(deviceDefinitions):
  validateConfiguration(deviceDefinitions)
  
  devices = {

  }

  for device in deviceDefinitions:
    print(device)
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
  return devices



def validateConfiguration(deviceConfigs):
  deviceDict = {

  }
  for device in deviceConfigs:

    if deviceDict.get(device['id'], None) == None:
      deviceDict[device['id']] = device
    else:
      raise Exception("Duplicate device id {0}".format(device['id']))
  
  return False
