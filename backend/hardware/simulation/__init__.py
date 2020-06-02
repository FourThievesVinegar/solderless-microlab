"""
Simulates the actual hardware. This is the package used by the unit tests.
"""

import time
import config

heating = False
cooling = False
stirring = False
temperature = -1
timer = time.time();


def log(message):
    print('harware.simulation - ' + str(message))


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
    Sets the heater flag for the simulation.

    :return:
    None
    """
    global heating
    log('Turning on heat')
    heating = True


def turnHeaterOff():
    """
    Un-sets the heater flag for the simulation.

    :return:
    None
    """
    global heating
    log('Turning off heat')
    heating = False


def turnCoolerOn():
    """
    Sets the cooler flag for the simulation.

    :return:
    None
    """
    global cooling
    log('Turning on cooling')
    cooling = True


def turnCoolerOff():
    """
    Un-sets the heater flag for the simulation.

    :return:
    None
    """
    global cooling
    log('Turning off cooling')
    cooling = False


def getTemp():
    """
    Simulates and returns temperature.

    Temperature starts off at 24C and changes every time the function is called as follows:
        heater flag on: +1C
        heater flag off: -0.1C
    :return:
    """
    global temperature, heating
    if temperature == -1:
        temperature = 24
    else:
        if heating == True:
            temperature = temperature + 1
        elif cooling == True:
            temperature = temperature - 1
        else:
            if temperature > 24:
                temperature = temperature - 0.1
            elif temperature < 24:
                temperature = temperature + 0.1
    print('Temperature read as: ' + str(temperature))
    return temperature


def turnStirrerOn():
    """
    Sets the stirrer flag for the simulation.

    :return:
    None
    """
    global stirring
    log('Starting to stir liquid')
    stirring = True


def turnStirrerOff():
    """
    Un-sets the stirrer flag for the simulation.

    :return:
    None
    """
    global stirring
    log('Stirring stopped')
    stirring = False


def pumpDispense(pumpId,volume):
    """
    Displays pump dispensing message.

    :param pumpId:
        The pump id. One of 'A' or 'B'
    :param volume:
        The number ml to dispense
    :return:
        None
    """
    if pumpId == 'A':
        log('Dispensing ' + str(volume) + 'ml from pump A')
    elif pumpId == 'B':
        log('Dispensing ' + str(volume) + 'ml from pump B')
