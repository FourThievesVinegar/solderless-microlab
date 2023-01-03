"""
The hardware package simply routes hardware calls to the appropriate python package that does the actual work.
The hardware package is configured in config.hardwarePackage and it must implement the methods as defined in
hardware.interface and used in this module below.
"""

import config
import hardware.reagentdispenser as rd
import hardware.stirring as stirring
import hardware.temperaturecontroller as tc

tempController = tc.createTemperatureController(config.tempControllerType, config.tempControllerArgs)
stirrer = stirring.createStirrer(config.stirrerType, config.stirrerArgs)
reagentDispenser = rd.createReagentDispenser(config.reagentdispenserType, config.reagentDispenserArgs)

timer = time.time();

def log(message):
    """
    Log a debug message.

    :param message:
        The actual message

    :return:
        None
    """
    print('hardware - {0}'.format(message))


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
