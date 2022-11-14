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
hardwareCoolearPin = environ.get("COOLER_PIN", 26)
hardwareStirrerPin = environ.get("STIRRER_PIN", 20)

# port for Arduino... again need to auto-detect as the temp sensor may or may not be detected first
hardwareArduinoPort = environ.get("ARDUINO_PORT", '/dev/ttyUSB0') 
hardwarePumpAGcode1ml = b'G91X1.1\n'
hardwarePumpAGcodeRetract = b'G91X-0.25\n'
hardwarePumpBGcode1ml = b'G91Y1.1\n'
hardwarePumpBGcodeRetract = b'G91Y-0.25\n'

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
