import hardware.stirring as stirrer
import hardware.reagentdispenser as rd
import hardware.temperaturecontroller as tc
import hardware.thermometer as thermometer
import hardware.gpiochip as gpiochip
import config
import yaml
from os.path import exists

def loadHardwareConfiguration():
  if config.hardwareBoard != "custom":
    path = './hardware/boardhardwareconfig/{0}.yaml'.format(config.hardwareBoard)
    if not exists(path):
      raise Exception("No board configuration found for '{0}'".format(config.hardwareBoard))
    boardHardware = yaml.safe_load(open(path, 'r'))
  else:
    boardHardware = {"devices": []}


  userHardware = yaml.safe_load(open('./hardware/base_hardware.yaml', 'r'))

  return { "devices": boardHardware["devices"] + userHardware["devices"]}


def setupDevices():
  hardwareConfig = loadHardwareConfiguration()
  deviceDefinitions = hardwareConfig['devices']
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
      raise Exception("Duplicate device id {1}".format(device['id']))
  
  return False