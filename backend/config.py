from os import environ
"""
This is the config file. See the comments for each option.
"""

# The Host and port that the backend API is running on
apiHost = environ.get("API_HOST", 'localhost')  
apiPort = environ.get("API_PORT", 8081)  

# The URL used by the celery backend to update the state in the app.
localUrl = 'http://%s:%s' % (apiHost, apiPort)

# Which hardware implementation to use. Currently only 'real' or 'simulation' are supported.
#hardwarePackage = 'real'
hardwarePackage = environ.get("HARDWARE_PACKAGE", 'simulation')  
hardwareSpeedup = environ.get("HARDWARE_SPEEDUP", 10)  

# port for temperature sensor... eventually we want to automatically detect this
hardwareTempPort = environ.get("TEMP_PORT", '/dev/ttyUSB1')
hardwareHeaterPumpPin = environ.get("HEATER_PUMP_PIN", 16)  
hardwareHeaterPin = environ.get("HEATER_PIN", 19)  
hardwareCoolerPin = environ.get("COOLER_PIN", 26)
hardwareStirrerPin = environ.get("STIRRER_PIN", 20)

# port for Arduino... again need to auto-detect as the temp sensor may or may not be detected first
hardwareArduinoPort = environ.get("ARDUINO_PORT", '/dev/ttyACM0') 

syringePumpsConfig = {
  "X": {
    # Number of mm the stepper motor moves per full revolution, 
    # this is the pitch of the threaded rod
    "mmPerRev": environ.get("SYRINGE_PUMP_X_MM_PER_REV", 0.8),
    # Number of steps per revolution of the stepper motor, reference the documentation for the motor
    "stepsPerRev": environ.get("SYRINGE_PUMP_X_STEPS_PER_REV", 200),
    # Number of mm of movement needed to dispense 1 ml of fluid, 
    # this is the length of the syringe divided by its fluid capacity
    "mmPerml": environ.get("SYRINGE_PUMP_X_MM_PER_ML", 3.5),
    # Maximum speed the motor should run in mm/min
    "maxmmPerMin": environ.get("SYRINGE_PUMP_X_MAX_MM_PER_MIN", 240),
  },
  "Y": {
    "mmPerRev": environ.get("SYRINGE_PUMP_Y_MM_PER_REV", 0.8),
    "stepsPerRev": environ.get("SYRINGE_PUMP_Y_STEPS_PER_REV", 200),
    "mmPerml": environ.get("SYRINGE_PUMP_Y_MM_PER_ML", 3.5),
    "maxmmPerMin": environ.get("SYRINGE_PUMP_Y_MAX_MM_PER_MIN", 240),
  },
}

# Where the recipe files are located. You should never need to change this.
recipesPackage = environ.get("RECIPES_PACKAGE", 'recipes.files')  

# Celery configuration. You should never need to change this.
# 'real' and 'test' are supported. In 'test' mode
# it doesn't actually send the requests to the celery
# server it just runs them in the same thread. This is
# only useful for testing
celeryMode = environ.get("CELERY_MODE", 'real')     

redisHost = environ.get("REDIS_HOST", 'localhost')  
redisPort = environ.get("REDIS_PORT", 6379)  

celeryBackend = 'redis://%s:%s/0' % (redisHost, redisPort)
celeryBroker = 'redis://%s:%s/0' % (redisHost, redisPort)
