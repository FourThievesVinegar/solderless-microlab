import config
from hardware import interface as hw

exec('from hardware import ' + config.hardwarePackage + ' as hw')

def log(message):
    hw.log(message)

def sleep(seconds):
    hw.sleep(seconds)

def turnHeatOn():
    hw.turnHeatOn()

def turnHeatOff():
    hw.turnHeatOff()

def getTemp():
    hw.getTemp()