from os import environ
"""
This is the config file. See the comments for each option.
"""
## GENERAL CONFIGURATION ##

# Where the recipe files are located. You should never need to change this.
recipesPackage = environ.get("RECIPES_PACKAGE", 'recipes.files')  


## FLASK CONFIGURATION ##

# The Host and port that the backend API is running on
apiHost = environ.get("API_HOST", 'localhost')  
apiPort = environ.get("API_PORT", 8081)  

# The URL used by the celery backend to update the state in the app.
localUrl = 'http://%s:%s' % (apiHost, apiPort)


## HARDWARE CONFIGURATION ##

# Speeds up every task for testing hardware. Should be set to 1 for actual use
hardwareSpeedup = environ.get("HARDWARE_SPEEDUP", 1)  

# Which temperature controller implementation to use
# Supported values: basic, simulation
# basic: Basic hardware setup using two sets of pumps and a heating element
#        some currently incomplete instructions for this are in docs/assembly
# simulation: Simulates temperature changes due to heater and cooler activation
tempControllerType = environ.get("TEMP_CONTROLLER_TYPE", "basic")
tempControllerArgs = {
  ## basic MODE ARGS

  # Type of thermometer to use for measuring the temp of the reactor
  # Supported values: w1_therm, serial
  # w1_therm: Supports the DS18S20, DS1822, DS18B20, DS28EA00 and DS1825/MAX31850K
  #           sensors using the 1 wire protocol. You'll need to add "dtoverlay=w1-gpio"
  #           to /boot/config.txt and reboot to use this
  # serial: reads the sensor data from a serial device
  "thermometerType": environ.get("TEMP_CONTROLLER.THERMOMETER_TYPE", "w1_therm"),
  "thermometerArgs": {
    ## w1_therm MODE ARGS
    # None needed or supported at the moment

    ## serial MODE ARGS
    # Which device to read data from.
    "serialDevice": '/dev/ttyUSB1'
  },
  # GPIO pin for activating the heating element
  "heaterPin": environ.get("TEMP_CONTROLLER.GPIO_HEATER_PIN", 26),
  # GPIO pin for activating the heater pump(s)
  "heaterPumpPin": environ.get("TEMP_CONTROLLER.GPIO_HEATER_PUMP_PIN", 20),
  # GPIO pin for activating the cooler pump(s)
  "coolerPin": environ.get("TEMP_CONTROLLER.GPIO_COOLER_PIN", 21),

  ## simulation MODE ARGS
  # None needed or supported at the moment
}

# Which stirrer implementation to use
# Supported values: gpio_stirrer, simulation
# gpio_stirrer: activates the stirrer by switching a gpio pin
# simulation: Does nothing
stirrerType = environ.get("STIRRER_TYPE", "gpio_stirrer")
stirrerArgs = {
  ## gpio_stirrer MODE ARGS
  # GPIO pin for activating the stirrer
  "stirrerPin": environ.get("STIRRER_PIN", 16)

  ## simulation MODE ARGS
  # None needed or supported at the moment
}


# Which reagent dispenser implementation to use
# Supported values: syringepump, simulation
# syringepump: The open source syringe pump referenced in the assembly documentation
#              Uses grbl and stepper motors to dispense the reagents into the microlab
# simulation: Does nothing but sleep to simulate dispensing a reagent
reagentdispenserType = environ.get("REAGENT_DISPENSER_TYPE", "simulation")
reagentDispenserArgs = {
  ## syringepump MODE ARGS
  # Serial device for communication with the Arduino
  "arduinoPort": environ.get("ARDUINO_PORT", '/dev/ttyACM0'),
  # Configuration for the syringe pump motors
  "syringePumpsConfig": {
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
      # These are all the same as documented above but for the Y axis
      "mmPerRev": environ.get("SYRINGE_PUMP_Y_MM_PER_REV", 0.8),
      "stepsPerRev": environ.get("SYRINGE_PUMP_Y_STEPS_PER_REV", 200),
      "mmPerml": environ.get("SYRINGE_PUMP_Y_MM_PER_ML", 3.5),
      "maxmmPerMin": environ.get("SYRINGE_PUMP_Y_MAX_MM_PER_MIN", 240),
    },
  }
  ## simulation MODE ARGS
  # None needed or supported at the moment
}


## CELERY CONFIGURATION ##

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
