import hardware.stirring as stirrer
import hardware.reagentdispenser as rd
import hardware.temperaturecontroller as tc
import hardware.thermometer as thermometer


def setupDevices(hardwareConfig):
  print(hardwareConfig)
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