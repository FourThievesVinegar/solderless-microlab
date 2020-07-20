# TODO: Need to add in real code to control device here

import time
import config
import serial
import RPi.GPIO as GPIO

# Init timer for secondsSinceStart()
timer = time.time();

# Init serial port for temp sensor
ser = serial.Serial(config.hardwareTempPort)

# Init relays
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(config.hardwareHeaterPin, GPIO.OUT)
GPIO.setup(config.hardwareCoolearPin, GPIO.OUT)
GPIO.setup(config.hardwareStirrerPin, GPIO.OUT)

RELAY_ON = False
RELAY_OFF = True


def log(message):
    print('harware.simulation - ' + str(message))

def secondSinceStart():
    """
    The number of seconds since this package was started.

    This method is modified in the simulation package to allow for speeding up time without modifying the recipes.

    :return:
    The number of seconds since this package was started.
    """
    elapsed = time.time() - timer
    return elapsed


def sleep(seconds):
    """
    Sleep for a number of seconds.

    This method is modified in the simulation package to allow for speeding up time without modifying the recipes.

    :param seconds:
    Number of seconds to sleep.

    :return:
    None
    """
    time.sleep(seconds)


def turnHeaterOn():
    """
    Turns heater on.

    :return:
    None
    """
    GPIO.output(config.hardwareHeaterPin, RELAY_ON)


def turnHeaterOff():
    """
    Turns heater off.

    :return:
    None
    """
    GPIO.output(config.hardwareHeaterPin, RELAY_OFF)


def turnCoolerOn():
    """
    Turn cooler on.

    :return:
    None
    """
    GPIO.output(config.hardwareCoolearPin, RELAY_ON)


def turnCoolerOff():
    """
    Turn cooler off.

    :return:
    None
    """
    GPIO.output(config.hardwareCoolearPin, RELAY_OFF)


def getTemp():
    """
    Read the temperature from the temperature sensor.
    :return:
    The temperature of the temperature sensor.
    """
    while (ser.read(1)[0] != 116):
        a = 1
    ser.read(2)
    sign = -1
    if (ser.read(1)[0] == 43):
        sign = 1
    temperature = sign * float(ser.read(5).decode("ascii"))

    return temperature


def turnStirrerOn():
    """
    Turns the stirrer on.

    :return:
    None
    """
    GPIO.output(config.hardwareStirrerPin, RELAY_ON)


def turnStirrerOff():
    """
    Turns the stirrer off.

    :return:
    None
    """
    GPIO.output(config.hardwareStirrerPin, RELAY_OFF)


def pumpDispense(pumpId,volume):
    """
    Dispense reagent from a siringe

    :param pumpId:
        The pump id. One of 'A' or 'B'
    :param volume:
        The number ml to dispense
    :return:
        None
    """
    a = 1