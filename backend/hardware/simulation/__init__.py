import time
import config

heater = False
temperature = -1

def log(message):
    print('harware.simulation - ' + str(message))

def sleep(seconds):
    if hasattr(config,'hardwareSpeedup'):
        speed = config.hardwareSpeedup
        if not (speed == None):
            time.sleep(seconds/speed)
            return

    time.sleep(seconds)

def turnHeatOn():
    log('Turning on heat')
    heater = True

def turnHeatOff():
    log('Turning off heat')
    heater = False

def getTemp():
    global temperature
    if temperature == -1:
        temperature = 24
    else:
        if heater == True:
            temperature = temperature + 1
        else:
            temperature = temperature - 1
            if temperature < 24:
                temperature = 24
    return temperature