"""
This is the config file. See the comments for each option.
"""

# The URL used by the celery backend to update the state in the app.
localUrl = 'http://localhost:8081/'

# Which hardware implementation to use. Currently only 'real' or 'simulation' are supported.
#hardwarePackage = 'real'
hardwarePackage = 'simulation'
hardwareSpeedup = 10

# port for temperature sensor... eventually we want to automatically detect this
hardwareTempPort = '/dev/ttyUSB1'
hardwareHeaterPin = 19
hardwareCoolearPin = 26
hardwareStirrerPin = 20

# port for Arduino... again need to auto-detect as the temp sensor may or may not be detected first
hardwareArduinoPort = '/dev/ttyUSB0'
hardwarePumpAGcode1ml = b'G91X1.1\n'
hardwarePumpAGcodeRetract = b'G91X-0.25\n'
hardwarePumpBGcode1ml = b'G91Y1.1\n'
hardwarePumpBGcodeRetract = b'G91Y-0.25\n'

# Where the recipe files are located. You should never need to change this.
recipesPackage = 'recipes.files'

# Celery configuration. You should never need to change this.
celeryMode = 'real'     # 'real' and 'test' are supported. In 'test' mode
                        # it doesn't actually send the requests to the celery
                        # server it just runs them in the same thread. This is
                        # only useful for testing
celeryBackend = 'redis://localhost:6379/0'
celeryBroker = 'redis://localhost:6379/0'
