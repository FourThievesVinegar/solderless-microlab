from recipes import celery
from hardware import microlab


def heat(parameters):
    """
    Turn on the heater and reach a target temperature.

    :param parameters:
        dictionary
            'temp' - the desired temperature
    :return:
        None
    """
    targetTemp = parameters['temp']
    celery.logger.info('heating water to {0}...'.format(targetTemp))
    microlab.turnHeaterOn()
    while microlab.getTemp() < targetTemp:
        microlab.sleep(0.5)
    microlab.turnHeaterOff()


def cool(parameters):
    """
    Turn on the cooler and reach a target temperature.

    :param parameters:
        dictionary
            'temp' - the desired temperature
    :return:
        None
    """
    targetTemp = parameters['temp']
    celery.logger.info('cooling water to {0}...'.format(targetTemp))
    microlab.turnCoolerOn()
    while microlab.getTemp() > targetTemp:
        microlab.sleep(0.5)
    microlab.turnCoolerOff()


def maintainCool(parameters):
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
    maintain(parameters)


def maintainHeat(parameters):
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
    maintain(parameters)


def maintain(parameters):
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

    while (microlab.secondSinceStart() - start) < duration:
        microlab.sleep(interval)
        currentTemp = microlab.getTemp()
        celery.logger.info('temperature @ {0}'.format(currentTemp))
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

    microlab.turnHeaterOff()
    microlab.turnCoolerOff()


def pump(parameters):
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
    microlab.pumpDispense(pump, volume)


def stir(parameters):
    """
    Turn on the stirrer for a predefined amount of time.

    :param parameters:
        dictionary
            'time' - the amount of time to turn on the stirrer for
    :return:
        None
    """
    duration = parameters['time']

    interval = 0.5
    start = microlab.secondSinceStart()
    microlab.turnStirrerOn()
    while (microlab.secondSinceStart() - start) < duration:
        microlab.sleep(interval)
    microlab.turnStirrerOff()



tasks = {
  'heat': heat,
  'cool': cool,
  'maintainCool': maintainCool,
  'maintainHeat': maintainHeat,
  'maintain': maintain,
  'pump': pump,
  'stir': stir,
}