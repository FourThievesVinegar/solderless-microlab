"""
This is the config file. See the comments for each option.
"""

# The URL used by the celery backend to update the state in the app.
localUrl = 'http://localhost:5000/'

# Which hardware implementation to use. Currently only 'real' or 'simulation' are supported.
#hardwarePackage = 'real'
hardwarePackage = 'simulation'

# Where the recipe files are located. You should never need to change this.
recipesPackage = 'recipes.files'

# Celery configuration. You should never need to change this.
celeryMode = 'real'     # 'real' and 'test' are supported. In 'test' mode
                        # it doesn't actually send the requests to the celery
                        # server it just runs them in the same thread. This is
                        # only useful for testing
celeryBackend = 'redis://localhost:6379/0'
celeryBroker = 'redis://localhost:6379/0'
