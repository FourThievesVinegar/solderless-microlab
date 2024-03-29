"""
List of tasks available for recipes to execute. All tasks must take
an instance of MicroLabHardware as their first argument, and a dictionary
with whatever needed arguments as their second. 

All tasks must return an iterator that executes one iteration of the task
per call of next(), returning None when execution has finished, or
a number in seconds (decimals are allowed) for when to next execute the task.
"""

from datetime import datetime
import logging

def heat(microlab, parameters):
    """
    Turn on the heater and reach a target temperature.

    :param parameters:
        dictionary
            'temp' - the desired temperature
    :return:
        None
    """
    targetTemp = parameters['temp']
    logging.info('heating water to {0}...'.format(targetTemp))
    microlab.turnHeaterOn()
    while True:
        if microlab.getTemp() >= targetTemp:
            microlab.turnHeaterOff()
            yield None
        yield 1


def cool(microlab, parameters):
    """
    Turn on the cooler and reach a target temperature.

    :param parameters:
        dictionary
            'temp' - the desired temperature
    :return:
        None
    """
    targetTemp = parameters['temp']
    logging.info('cooling water to {0}...'.format(targetTemp))
    microlab.turnCoolerOn()
    while True:
        if microlab.getTemp() <= targetTemp:
            microlab.turnCoolerOff()
            yield None
        yield 1


def maintainCool(microlab, parameters):
    """
    Maintain a certain temperature using the cooler for a specified amount of time.

    :param parameters:
        dictionary
            'temp' - the desired temperature
            'tolerance' - how much above or below the desired temperature to let
                            the temperature drift before turning on cooler again
            'time' - the amount of time to maintain the temperature in seconds
    :return:
        None
    """
    parameters['type'] = 'cool'
    return maintain(microlab, parameters)


def maintainHeat(microlab, parameters):
    """
    Maintain a certain temperature using the heater for a specified amount of time.

    :param parameters:
        dictionary
            'temp' - the desired temperature
            'tolerance' - how much above or below the desired temperature to let
                            the temperature drift before turning on heater again
            'time' - the amount of time to maintain the temperature in seconds
    :return:
        None
    """
    parameters['type'] = 'heat'
    return maintain(microlab, parameters)


def maintain(microlab, parameters):
    """
    Maintain a certain temperature using either the cooler or heater for a specified amount of time.

    :param parameters:
        dictionary
            'temp' - the desired temperature
            'tolerance' - how much above or below the desired temperature to let
                            the temperature drift before turning on the heater/cooler again
            'time' - the amount of time to maintain the temperature in seconds
            'type' - one of:
                - heat
                    Maintain temperature using heater.
                - cool
                    Maintain temperature using cooler.
    :return:
        None
    """
    duration = parameters['time']
    targetTemp = parameters['temp']
    tolerance = parameters['tolerance']
    type = parameters['type']

    interval = 0.5
    start = microlab.secondSinceStart()

    logging.info('Maintaining {0}C for {1} seconds with {2}C tolerance'.format(targetTemp, duration, tolerance))

    while True:
        currentTemp = microlab.getTemp()
        logging.debug('temperature @ {0}'.format(currentTemp))
        if (microlab.secondSinceStart() - start) >= duration:
            microlab.turnHeaterOff()
            microlab.turnCoolerOff()
            yield None
        if currentTemp - tolerance > targetTemp:
            if type == 'heat':
                microlab.turnHeaterOff()
            else:
                microlab.turnCoolerOn()
        if currentTemp + tolerance < targetTemp:
            if type == 'heat':
                microlab.turnHeaterOn()
            else:
                microlab.turnCoolerOff()

        yield interval


def pump(microlab, parameters):
    """
    Dispense a certain amount of liquid from a pump.

    :param parameters:
        dictionary
            'pump' - one of: 'X' or 'Y' or 'Z'
            'volume' - volume to dispense in ml
    :return:
        None
    """
    pump = parameters['pump']
    volume = parameters['volume']
    logging.info('Dispensing {0}ml from pump {1}'.format(volume, pump))
    microlab.pumpDispense(pump, volume)
    yield None


def stir(microlab, parameters):
    """
    Turn on the stirrer for a predefined amount of time.

    :param parameters:
        dictionary
            'time' - the amount of time to turn on the stirrer for
    :return:
        None
    """
    duration = parameters['time']
    logging.info('Stirring for {0} seconds'.format(duration))
    start = microlab.secondSinceStart()
    microlab.turnStirrerOn()
    while True:
        if (microlab.secondSinceStart() - start) >= duration:
            microlab.turnStirrerOff()
            yield None
        yield 1




tasks = {
  'heat': heat,
  'cool': cool,
  'maintainCool': maintainCool,
  'maintainHeat': maintainHeat,
  'maintain': maintain,
  'pump': pump,
  'stir': stir,
}

def runTask(microlab, task, parameters):
    """
    Create an iterator for running a task.

    :param microlab:
        The microlab hardware interface

    :param task:
        Task to run under the currently running recipe.

    :param parameters:
        Parameters to pass to the task. The actual object definition depends on the task.

    :return:
        An iterator that executes one tick of a task per call of next()
    """
    return {
        "fn": tasks[task](microlab, parameters),
        "parameters": parameters,
        "done": False,
        "nextTime": datetime.now()
    }
