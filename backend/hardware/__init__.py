import config
from hardware import interface as hw

exec('from hardware import ' + config.hardwarePackage + ' as hw')

def log(message):
    hw.log(message)


def secondSinceStart():
    return hw.secondSinceStart()


def sleep(seconds):
    hw.sleep(seconds)


def turnHeatOn():
    hw.turnHeatOn()


def turnHeatOff():
    hw.turnHeatOff()


def getTemp():
    return hw.getTemp()