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
from simple_pid import PID

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
    microlab.turnHeaterPumpOn()
    while True:
        if microlab.getTemp() >= targetTemp:
            microlab.turnHeaterOff()
            microlab.turnHeaterPumpOff()
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
    Maintain a certain temperature using the cooler and/or heater for a specified amount of time.

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
                - both
                    Maintain temperature using heater and cooler.
                    Default if not otherwise specified
    :return:
        None
    """
    if microlab.getPIDConfig() is None:
        return maintainSimple(microlab, parameters)
    else:
        return maintainPID(microlab, parameters)


def maintainSimple(microlab, parameters):
    """
    Maintain a certain temperature using the cooler and/or heater for a specified amount of time.

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
                - both
                    Maintain temperature using heater and cooler.
                    Default if not otherwise specified
    :return:
        None
    """
    duration = parameters['time']
    targetTemp = parameters['temp']
    tolerance = parameters['tolerance']
    if 'type' in parameters:
        maintainType = parameters['type']
    else:
        maintainType =  'both'
    heaterEnabled = (maintainType == 'heat' or maintainType == 'both')
    coolerEnabled = (maintainType == 'cool' or maintainType == 'both')

    interval = 0.5
    start = microlab.secondSinceStart()

    logging.info('Maintaining {0}C for {1} seconds with {2}C tolerance'.format(targetTemp, duration, tolerance))
    # default temp control
    logging.debug('Maintaining with default temperature control')

    while True:
        currentTemp = microlab.getTemp()
        logging.debug('temperature @ {0}'.format(currentTemp))
        if (microlab.secondSinceStart() - start) >= duration:
            microlab.turnHeaterOff()
            microlab.turnHeaterPumpOff()
            microlab.turnCoolerOff()
            yield None
        if heaterEnabled:
            if currentTemp > targetTemp:
                microlab.turnHeaterOff()
                microlab.turnHeaterPumpOff()
            if currentTemp < targetTemp - tolerance:
                microlab.turnHeaterOn()
                microlab.turnHeaterPumpOn()
        if coolerEnabled:
            if currentTemp > targetTemp + tolerance:
                microlab.turnCoolerOn()
            if currentTemp < targetTemp:
                microlab.turnCoolerOff()

        yield interval

            
def maintainPID(microlab, parameters):
    """
    Maintain a certain temperature using the cooler and/or heater for a specified amount of time.
    Uses a PID control loop.

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
                - both
                    Maintain temperature using heater and cooler.
                    Default if not otherwise specified
    :return:
        None
    """
    duration = parameters['time']
    targetTemp = parameters['temp']
    tolerance = parameters['tolerance']
    if 'type' in parameters:
        maintainType = parameters['type']
    else:
        maintainType =  'both'
    heaterEnabled = (maintainType == 'heat' or maintainType == 'both')
    coolerEnabled = (maintainType == 'cool' or maintainType == 'both')

    start = microlab.secondSinceStart()

    logging.info('Maintaining {0}C for {1} seconds with {2}C tolerance'.format(targetTemp, duration, tolerance))
    logging.debug('Maintaining with PID temperature control')

    pidConfig = microlab.getPIDConfig()
    pid = PID(pidConfig['P'], pidConfig['I'], pidConfig['D'], setpoint=targetTemp)
    maxOutput = pidConfig['maxOutput']
    minOutput = pidConfig['minOutput']
    pid.output_limits = (minOutput, maxOutput)
    if pidConfig['proportionalOnMeasurement'] == True:
        pid.proportional_on_measurement = True
    if pidConfig['differentialOnMeasurement'] == False:
        pid.differential_on_measurement = False

    dutyCycleLength = pidConfig['dutyCycleLength']
    heaterCycleSecond = dutyCycleLength/maxOutput
    coolerCycleSecond = dutyCycleLength/minOutput

    microlab.turnHeaterPumpOn()
    while True:
        currentTemp = microlab.getTemp()
        control = pid(currentTemp)
        p, i, d = pid.components
        logging.info('Heater PID values: {} {} {} {} {}'.format(currentTemp, control, p, i, d))
            
        # We split the duty cycle length up into 1 second boxes,
        # based on the control value, duty cycle length, and
        # max/min outputs we enable the heater or cooler for
        # control/(max or minOutput) percent of the duty cycle,
        # rounded to the nearest second
        for i in range(1, dutyCycleLength):
            if heaterEnabled:
                if control * heaterCycleSecond > i:
                    microlab.turnHeaterOn()
                else:
                    microlab.turnHeaterOff()

            if coolerEnabled:
                if control * coolerCycleSecond > i:
                    microlab.turnCoolerOn()
                else:
                    microlab.turnCoolerOff()

            yield 1
            t = microlab.getTemp()
            a = pid(t)
            p, i, d = pid.components
            logging.debug('Heater PID values: {} {} {} {} {}'.format(t, a, p, i, d))
            
        
        if (microlab.secondSinceStart() - start) >= duration:
            microlab.turnHeaterOff()
            microlab.turnHeaterPumpOff()
            microlab.turnCoolerOff()
            yield None
        yield 1
        

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
    duration = parameters.get('duration', None)
    logging.info('Dispensing {0}ml from pump {1}'.format(volume, pump))
    pumpSpeedLimits = microlab.getPumpSpeedLimits(pump)
    minSpeed = pumpSpeedLimits["minSpeed"]
    maxSpeed = pumpSpeedLimits["maxSpeed"]
    mlPerSecond = maxSpeed
    if duration:
        mlPerSecond = volume/duration
    
    if mlPerSecond > maxSpeed:
        raise Exception("Recipe task cannot be completed, pump {0} cannot operate fast enough.".format(pump))
    elif mlPerSecond >= minSpeed and mlPerSecond <= maxSpeed:
        dispenseTime = microlab.pumpDispense(pump, volume, duration)
        yield dispenseTime
        yield None
    # If desired dispense speed is below what the pump can physically support,
    # dispense in 1 seconds bursts at slowest possible speed, waiting
    # for required time to emulate slower dispensing speed.
    elif mlPerSecond < minSpeed:
        onTime = mlPerSecond/minSpeed
        volumeDispensed = 0
        while volumeDispensed + minSpeed < volume:
            startTime = microlab.secondSinceStart()
            microlab.pumpDispense(pump, minSpeed, 1)
            volumeDispensed += minSpeed
            # Keep track of and subtract off execution time
            # from the total time taken for each step.
            # helps keep the actual task completion time more accurate
            # to desired duration
            executionTime = (microlab.secondSinceStart()-startTime)
            logging.debug('dispense exeuction time: {0}'.format(executionTime))
            yield 1/onTime - executionTime
        # dispense remaining volume
        remaining = volume-volumeDispensed
        microlab.pumpDispense(pump, remaining)
        # shorten duration based on amount that remains to be dispensed
        yield (1/onTime) * remaining/minSpeed
        yield None

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
