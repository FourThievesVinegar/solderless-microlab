"""
The hardware package simply routes hardware calls to the appropriate python package that does the actual work.
The hardware package is configured in config.hardwarePackage and it must implement the methods as defined in
hardware.interface and used in this module below.
"""

import config
from hardware import interface as hw

# Point the hw package to the implementation as configured in config.hardwarePackage.
exec('from hardware import ' + config.hardwarePackage + ' as hw')

def log(message):
    """
    Log a debug message.

    Since this is going to run through celery, the hw package is responsible for putting these messages
    somewhere sensible. Look at the implementation for details.

    :param message:
    The actual message

    :return:
    None
    """
    hw.log(message)


def secondSinceStart():
    """
    Get the number of seconds that have elapsed since the hardware module was started.

    The point of this method is to allow for speeding up time without modifying the recipes. This
    is especially useful for testing. In the final hardware implementation this can simply return
    the unix epoch.

    :return:
    Number of seconds since the hardware module was started... or unix epoch.
    """
    return hw.secondSinceStart()


def sleep(seconds):
    """
    Sleep for a number of seconds.

    The point of this method is to allow for speeding up time without modifying the recipes. This
    is especially useful for testing. In the final hardware implementation this can time.sleep

    :param seconds:
    Number of seconds to sleep.

    :return:
    None
    """
    hw.sleep(seconds)


def turnHeatOn():
    """
    Start heating the jacket.

    :return:
    None
    """
    hw.turnHeatOn()


def turnHeatOff():
    """
    Stop heating the jacket.

    :return:
    None
    """
    hw.turnHeatOff()


def getTemp():
    """
    Return the temperature.

    :return:
    The temperature as read from the sensor in Celsius
    """
    return hw.getTemp()