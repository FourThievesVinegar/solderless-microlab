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

# Which hardware board the software is being run on, for loading known hardware configuration. 
# supported values:
# pi, AML-S905X-CC-V1.0A, hardware_simulation, custom
# Custom loads nothing. All hardware used must then be specified in base_hardware.yaml 
hardwareBoard = environ.get("HARDWARE_BOARD", "pi")  

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
