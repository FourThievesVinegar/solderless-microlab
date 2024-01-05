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


## HARDWARE CONFIGURATION ##

# Speeds up every task for testing hardware. Should be set to 1 for actual use
hardwareSpeedup = environ.get("HARDWARE_SPEEDUP", 1)  

# Which hardware board the software is being run on, for loading known hardware configuration. 
# supported values:
# pi, AML-S905X-CC-V1.0A, hardware_simulation, custom
# Custom loads nothing. All hardware used must then be specified in base_hardware.yaml 
hardwareBoard = environ.get("HARDWARE_BOARD", "pi")  


