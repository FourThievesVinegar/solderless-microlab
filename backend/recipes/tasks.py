"""
List of tasks available for recipes to execute. All tasks must take
an instance of MicroLabHardware as their first argument, and a dictionary
with whatever needed arguments as their second.

All tasks must return an iterator that executes one iteration of the task
per call of next(), returning None when execution has finished, or
a number in seconds (decimals are allowed) for when to next execute the task.
"""

from datetime import datetime
from typing import Optional, Any, Generator, Callable

from simple_pid import PID

from hardware.core import MicroLabHardware
from localization import load_translation
from recipes.model import RecipeTaskRunnable
from util.logger import MultiprocessingLogger


def heat(microlab: MicroLabHardware, parameters: dict) -> Generator[Optional[float], Any, Any]:
    """
    Turn on the heater and reach a target temperature.

    :param microlab : MicroLabHardware
        The hardware interface used to control the heater.
    :param parameters : dict
        A dictionary containing:
        * 'temp' (float) – The desired target temperature in degrees Celsius.
    :yields:
        Optional[float]
        * If the heating task is finished and no further scheduling is required, yield `None`.
        * Otherwise, yield a float indicating how many seconds to wait before this generator should be re‐invoked.
    """
    t = load_translation()

    logger = MultiprocessingLogger.get_logger(__name__)

    target_temp = parameters['temp']
    logger.info(t['heating-water'].format(target_temp))
    microlab.turnHeaterOn()
    microlab.turnHeaterPumpOn()
    while True:
        if microlab.getTemp() >= target_temp:
            microlab.turnHeaterOff()
            microlab.turnHeaterPumpOff()
            yield None
        yield 1.0


def cool(microlab: MicroLabHardware, parameters: dict) -> Generator[Optional[float], Any, Any]:
    """
    Turn on the cooler and reach a target temperature.

    :param microlab : MicroLabHardware
        The hardware interface used to control the cooler.
    :param parameters : dict
        A dictionary containing:
        * 'temp' (float) – The desired target temperature in degrees Celsius.
    :yields:
        Optional[float]
        * If the cooling task is finished and no further scheduling is required, yield `None`.
        * Otherwise, yield a float indicating how many seconds to wait before this generator should be re‐invoked.
    """
    t = load_translation()

    logger = MultiprocessingLogger.get_logger(__name__)

    target_temp = parameters['temp']
    logger.info(t['cooling-water'].format(target_temp))
    microlab.turnCoolerOn()
    while True:
        if microlab.getTemp() <= target_temp:
            microlab.turnCoolerOff()
            yield None
        yield 1.0


def maintain_cool(microlab: MicroLabHardware, parameters: dict) -> Generator[Optional[float], Any, Any]:
    """
    Maintain a certain temperature using the cooler for a specified amount of time.

    :param microlab : MicroLabHardware
        The hardware interface used to control the cooler.
    :param parameters : dict
        A dictionary containing:
            'temp' - the desired temperature
            'tolerance' - how much above or below the desired temperature to let
                            the temperature drift before turning on cooler again
            'time' - the amount of time to maintain the temperature in seconds
    :yields:
        Optional[float]
        * If the cooling task is finished and no further scheduling is required, yield `None`.
        * Otherwise, yield a float indicating how many seconds to wait before this generator should be re‐invoked.
    """
    parameters['type'] = 'cool'
    return maintain(microlab, parameters)


def maintain_heat(microlab: MicroLabHardware, parameters: dict) -> Generator[Optional[float], Any, Any]:
    """
    Maintain a certain temperature using the heater for a specified amount of time.

    :param microlab : MicroLabHardware
        The hardware interface used to control the heater.
    :param parameters : dict
        A dictionary containing:
            'temp' - the desired temperature
            'tolerance' - how much above or below the desired temperature to let
                            the temperature drift before turning on heater again
            'time' - the amount of time to maintain the temperature in seconds
    :yields:
        Optional[float]
        * If the heating task is finished and no further scheduling is required, yield `None`.
        * Otherwise, yield a float indicating how many seconds to wait before this generator should be re‐invoked.
    """
    parameters['type'] = 'heat'
    return maintain(microlab, parameters)


def maintain(microlab: MicroLabHardware, parameters: dict) -> Generator[Optional[float], Any, Any]:
    """
    Maintain a certain temperature using the cooler and/or heater for a specified amount of time.

    :param microlab : MicroLabHardware
        The hardware interface used to control the hardware
    :param parameters : dict
        A dictionary containing:
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
    :yields:
        Optional[float]
        * If the task is finished and no further scheduling is required, yield `None`.
        * Otherwise, yield a float indicating how many seconds to wait before this generator should be re‐invoked.
    """
    if microlab.getPIDConfig() is None:
        return maintain_simple(microlab, parameters)
    else:
        return maintain_pid(microlab, parameters)


def maintain_simple(microlab: MicroLabHardware, parameters: dict) -> Generator[Optional[float], Any, Any]:
    """
    Maintain a certain temperature using the cooler and/or heater for a specified amount of time.

    :param microlab : MicroLabHardware
        The hardware interface used to control the hardware
    :param parameters : dict
        A dictionary containing:
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
    :yields:
        Optional[float]
        * If the task is finished and no further scheduling is required, yield `None`.
        * Otherwise, yield a float indicating how many seconds to wait before this generator should be re‐invoked.
    """
    t = load_translation()
    logger = MultiprocessingLogger.get_logger(__name__)

    duration = parameters['time']
    target_temp = parameters['temp']
    tolerance = parameters['tolerance']
    maintain_type = parameters.get('type', 'both')
    heater_enabled = maintain_type in ('heat', 'both')
    cooler_enabled = maintain_type in ('cool', 'both')

    interval = 0.5
    start_time = microlab.uptime_seconds()

    logger.info(t['maintaining-specific-temperature'].format(target_temp, duration, tolerance))
    logger.debug(t['maintaining-default-temperature'])

    while True:
        current_temp = -9999.9999
        try:
            current_temp = microlab.getTemp()
            logger.debug(f'temperature @ {current_temp}')
            if (microlab.uptime_seconds() - start_time) >= duration:
                microlab.turnHeaterOff()
                microlab.turnHeaterPumpOff()
                microlab.turnCoolerOff()
                yield None

            if heater_enabled:
                if current_temp > target_temp:
                    microlab.turnHeaterOff()
                    microlab.turnHeaterPumpOff()
                elif current_temp < target_temp - tolerance:
                    microlab.turnHeaterOn()
                    microlab.turnHeaterPumpOn()
            if cooler_enabled:
                if current_temp > target_temp + tolerance:
                    microlab.turnCoolerOn()
                elif current_temp < target_temp:
                    microlab.turnCoolerOff()

            yield interval

        except Exception as e:
            logger.error(
                t['error-maintaining-temperature'].format(current_temp, target_temp, e)
            )


def maintain_pid(microlab: MicroLabHardware, parameters: dict) -> Generator[Optional[float], Any, Any]:
    """
    Maintain a certain temperature using the cooler and/or heater for a specified amount of time.
    Uses a PID control loop.

    :param microlab : MicroLabHardware
        The hardware interface used to control the hardware
    :param parameters : dict
        A dictionary containing:
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
    :yields:
        Optional[float]
        * If the task is finished and no further scheduling is required, yield `None`.
        * Otherwise, yield a float indicating how many seconds to wait before this generator should be re‐invoked.
    """
    translations = load_translation()  # not 't' for avoiding ambiguity with already present t variable
    logger = MultiprocessingLogger.get_logger(__name__)

    duration = parameters['time']
    target_temp = parameters['temp']
    tolerance = parameters['tolerance']
    maintain_type = parameters.get('type', 'both')
    heater_enabled = maintain_type in ('heat', 'both')
    cooler_enabled = maintain_type in ('cool', 'both')

    start_time = microlab.uptime_seconds()

    logger.info(
        translations['maintaining-specific-temperature'].format(target_temp, duration, tolerance)
    )
    logger.debug(translations['maintaning-PID-temperature'])

    pidConfig = microlab.getPIDConfig()
    pid = PID(pidConfig['P'], pidConfig['I'], pidConfig['D'], setpoint=target_temp)
    maxOutput = pidConfig['maxOutput']
    minOutput = pidConfig['minOutput']
    pid.output_limits = (minOutput, maxOutput)
    if pidConfig['proportionalOnMeasurement']:
        pid.proportional_on_measurement = True
    if not pidConfig['differentialOnMeasurement']:
        pid.differential_on_measurement = False

    dutyCycleLength = pidConfig['dutyCycleLength']
    heaterCycleSecond = dutyCycleLength / maxOutput
    coolerCycleSecond = dutyCycleLength / minOutput

    microlab.turnHeaterPumpOn()
    while True:
        currentTemp = microlab.getTemp()
        control = pid(currentTemp)
        p, i, d = pid.components
        logger.info(
            translations['heater-PID-values'].format(currentTemp, control, p, i, d)
        )

        # We split the duty cycle length up into 1 second boxes,
        # based on the control value, duty cycle length, and
        # max/min outputs we enable the heater or cooler for
        # control/(max or minOutput) percent of the duty cycle,
        # rounded to the nearest second
        for i in range(1, dutyCycleLength):
            if heater_enabled:
                if control * heaterCycleSecond > i:
                    microlab.turnHeaterOn()
                else:
                    microlab.turnHeaterOff()

            if cooler_enabled:
                if control * coolerCycleSecond > i:
                    microlab.turnCoolerOn()
                else:
                    microlab.turnCoolerOff()

            yield 1.0
            t = microlab.getTemp()
            a = pid(t)
            p, i, d = pid.components
            logger.debug(translations['heater-PID-values'].format(t, a, p, i, d))

        if (microlab.uptime_seconds() - start_time) >= duration:
            microlab.turnHeaterOff()
            microlab.turnHeaterPumpOff()
            microlab.turnCoolerOff()
            yield None
        yield 1.0


def pump(microlab: MicroLabHardware, parameters: dict) -> Generator[Optional[float], Any, Any]:
    """
    Dispense a certain amount of liquid from a pump.

    :param microlab : MicroLabHardware
        The hardware interface used to control the hardware
    :param parameters:
        dictionary
            'pump' - one of: 'X' or 'Y' or 'Z'
            'volume' - volume to dispense in ml
            'time' - optional, time to dispense volume over in seconds
    :yields:
        Optional[float]
        * If the task is finished and no further scheduling is required, yield `None`.
        * Otherwise, yield a float indicating how many seconds to wait before this generator should be re‐invoked.
    """
    t = load_translation()
    logger = MultiprocessingLogger.get_logger(__name__)

    pump_name = parameters['pump']
    target_volume = parameters['volume']
    duration = parameters.get('time')
    logger.info(t['dispensing'].format(target_volume, pump_name))

    limits = microlab.getPumpSpeedLimits(pump_name)
    min_rate, max_rate = limits['minSpeed'], limits['maxSpeed']
    rate = (target_volume / duration) if duration else max_rate

    # Fast‐or‐normal dispensing (rate >= min_rate)
    if rate >= min_rate:
        if rate > max_rate:
            logger.info(t['dispensing-max-speed'].format(pump_name))
            dispense_time = microlab.pumpDispense(pump_name, target_volume, None)
        else:
            dispense_time = microlab.pumpDispense(pump_name, target_volume, duration)
        yield dispense_time

    else:
        # If desired dispense speed is below what the pump can physically support,
        # dispense in 1 seconds bursts at slowest possible speed, waiting
        # for required time to emulate slower dispensing speed.
        # NOTE: subtracting 1.0 accounts for the one second that pump actually spend pumping each chunk at min_rate.
        interval = (min_rate / rate) - 1.0
        dispensed_volume = 0.0

        while dispensed_volume + min_rate < target_volume:
            start = microlab.uptime_seconds()
            microlab.pumpDispense(pump_name, min_rate, duration=1)
            dispensed_volume += min_rate

            exec_time = microlab.uptime_seconds() - start
            logger.debug(t['dispensing-time'].format(exec_time))

            # Wait the remainder of the burst cycle
            yield max(interval - exec_time, 0.0)

        # Dispense any remaining volume
        remaining_volume = target_volume - dispensed_volume
        if remaining_volume > 0:
            microlab.pumpDispense(pump_name, remaining_volume, duration=None)
            yield remaining_volume / rate

    # Signal completion exactly once
    yield None


def stir(microlab: MicroLabHardware, parameters: dict) -> Generator[Optional[float], Any, Any]:
    """
    Turn on the stirrer for a predefined amount of time.

    :param microlab : MicroLabHardware
        The hardware interface used to control the hardware
    :param parameters : dict
        A dictionary containing:
            'time' - the amount of time to turn on the stirrer for
    :return:
        None
    """
    t = load_translation()

    logger = MultiprocessingLogger.get_logger(__name__)

    duration = parameters['time']
    logger.info(t['stirring'].format(duration))
    start = microlab.uptime_seconds()
    microlab.turnStirrerOn()
    while True:
        if (microlab.uptime_seconds() - start) >= duration:
            microlab.turnStirrerOff()
            yield None
        yield 1.0


RECIPE_COMMANDS: dict[str, Callable[..., Generator[Optional[float], Any, Any]]] = {
    'heat': heat,
    'cool': cool,
    'maintainCool': maintain_cool,
    'maintainHeat': maintain_heat,
    'maintain': maintain,
    'pump': pump,
    'stir': stir,
}


def run_task(microlab: MicroLabHardware, task: str, parameters: dict) -> RecipeTaskRunnable:
    """
    Creates a generator for running a task.

    :param microlab:
        The microlab hardware interface

    :param task:
        Task to run under the currently running recipe.

    :param parameters:
        Parameters to pass to the task. The actual object definition depends on the task.

    :return:
        A `RecipeTaskRunnable` that has instantiated generator to execute one tick of a task per call of next()
    """
    fn: Callable[..., Generator[Optional[float], Any, Any]] = RECIPE_COMMANDS[task]
    return RecipeTaskRunnable(
        fn=fn(microlab, parameters),
        parameters=parameters,
        is_done=False,
        next_time=datetime.now(),
    )
