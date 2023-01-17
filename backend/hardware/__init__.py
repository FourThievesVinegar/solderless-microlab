"""
The hardware package acts as the interface for the software to interact with any hardware. Currently split into 3 different
distinct modules, the temperature controller, stirrer, and reagent dispenser, which contain the functions needed for 
controller the temperature of the reactor, stirring, and dispensing any reagents into the microlab respectively.
Alternative implementations just need to implement a new class withthe functions of the base class in the base.py file 
for the module, as well as adding a call to that for a unique string setting to the create function in the __init__.py
file.
"""

import time
import config
import yaml
import hardware.reagentdispenser as rd
import hardware.stirring as stirring
import hardware.temperaturecontroller as tc
from hardware import devicelist

devices = devicelist.setupDevices(yaml.safe_load(open('./hardware/base_hardware.yaml', 'r')))
tempController = devices['reactor-temperature-controller']
stirrer = devices['reactor-stirrer']
reagentDispenser = devices['reactor-reagent-dispenser']

timer = time.time();

def secondSinceStart():
    """
    The number of seconds since this package was started multiplied by config.hardwareSpeedup.

    This can effectively simulate time speedups for testing recipies.

    :return:
    The number of seconds since this package was started multiplied by config.hardwareSpeedup.
    """
    elapsed = time.time() - timer
    if hasattr(config,'hardwareSpeedup'):
        speed = config.hardwareSpeedup
        if not (speed == None):
            return elapsed * speed

    return elapsed


def sleep(seconds):
    """
    Sleep for a number of seconds or if config.harwareSpeedup is configured, for a number of
    seconds/config.hardwareSpeedup

    The point of this method is to allow for speeding up time without modifying the recipes. This
    is especially useful for testing.

    :param seconds:
    Number of seconds to sleep. In real life will actually sleep for seconds/config.hardwareSpeedup.

    :return:
    None
    """
    if hasattr(config,'hardwareSpeedup'):
        speed = config.hardwareSpeedup
        if not (speed == None):
            time.sleep(seconds/speed)
            return

    time.sleep(seconds)


def turnHeaterOn():
    """
    Start heating the jacket.

    :return:
        None
    """
    tempController.turnCoolerOff()
    tempController.turnHeaterOn()


def turnHeaterOff():
    """
    Stop heating the jacket.

    :return:
        None
    """
    tempController.turnHeaterOff()


def turnCoolerOn():
    """
    Start cooling the jacket.

    :return:
        None
    """
    tempController.turnHeaterOff()
    tempController.turnCoolerOn()


def turnCoolerOff():
    """
    Stop cooling the jacket.

    :return:
        None
    """
    tempController.turnCoolerOff()


def turnStirrerOn():
    """
    Start stirrer.

    :return:
        None
    """
    stirrer.turnStirrerOn()


def turnStirrerOff():
    """
    Start stirrer.

    :return:
        None
    """
    stirrer.turnStirrerOff()


def getTemp():
    """
    Return the temperature.

    :return:
        The temperature as read from the sensor in Celsius
    """
    return tempController.getTemp()


def pumpDispense(pumpId, volume):
    """
    Dispense a number of ml from a particular pump.

    :param pumpId:
        The pump id. One of 'X' or 'Y'
    :param volume:
        The number ml to dispense
    :return:
        None
    """
    return reagentDispenser.dispense(pumpId, volume)
