"""
Simulates the actual hardware. This is the package used by the unit tests.
"""

import time
import config

heater = False
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

def turnHeatOn():
    """
    Sets the heater flag for the simulation.

    :return:
    None
    """
    global heater
    log('Turning on heat')
    heater = True

def turnHeatOff():
    """
    Un-sets the heater flag for the simulation.

    :return:
    None
    """
    global heater
    log('Turning off heat')
    heater = False

def getTemp():
    """
    Simulates and returns temperature.

    Temperature starts off at 24C and changes every time the function is called as follows:
        heater flag on: +1C
        heater flag off: -0.1C
    :return:
    """
    global temperature, heater
    if temperature == -1:
        temperature = 24
    else:
        if heater == True:
            temperature = temperature + 1
        else:
            temperature = temperature - 0.1
            if temperature < 24:
                temperature = 24
    print('Temperature read as: ' + str(temperature))
    return temperature