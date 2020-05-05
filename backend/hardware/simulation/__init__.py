import time
import config

heater = False
temperature = -1
timer = time.time();

def log(message):
    print('harware.simulation - ' + str(message))


def secondSinceStart():
    elapsed = time.time() - timer
    if hasattr(config,'hardwareSpeedup'):
        speed = config.hardwareSpeedup
        if not (speed == None):
            return elapsed * speed

    return elapsed


def sleep(seconds):
    if hasattr(config,'hardwareSpeedup'):
        speed = config.hardwareSpeedup
        if not (speed == None):
            time.sleep(seconds/speed)
            return

    time.sleep(seconds)

def turnHeatOn():
    global heater
    log('Turning on heat')
    heater = True

def turnHeatOff():
    global heater
    log('Turning off heat')
    heater = False

def getTemp():
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