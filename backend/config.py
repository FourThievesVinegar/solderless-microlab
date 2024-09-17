"""
This file contains an interface for configuration loaded from and written to
disk and/or passed in as environment variables. Import and use this file with
"from config import microlabConfig as config"
Configuration is stored on disk at '/etc/microlab/microlab.ini'
"""
import os
import logging
from os import environ, makedirs, path
from configobj import ConfigObj, flatten_errors
from configobj.validate import Validator 
import shutil


class MicrolabConfig:
    """
    Contains all the microlab configuration values fetched from disk. Uses a
    class to abstract away setters to write to disk, and ability to reload
    changes from disk.
    """
    def __init__(self):
        vdt = Validator()

        configFileName = '/etc/microlab/microlab.ini'

        makedirs(path.dirname(configFileName), exist_ok=True)

        self.config = ConfigObj(configFileName, configspec="defaultconfig.ini")

        res = self.config.validate(vdt, copy=True, preserve_errors=True)

        self.config.write()

        for entry in flatten_errors(self.config, res):
            section_list, key, error = entry
            partialKey = self.config
            for section in section_list:
                partialKey = partialKey[section]
                default = partialKey.restore_default(key)

                if key is not None:
                    section_list.append(key)
                else:
                    section_list.append('[missing section]')
                section_string = '.'.join(section_list)
                if error == False:
                    error = 'Missing value or section.'
                logging.warning(
                    "Configuration error at {0}: '{1}', falling back to default value '{2}'."
                    .format(section_string, error, default))

    def reloadConfig(self):
        """
        Reloads microlab configuration from disk.
        """
        self.config.reload()

    ## GENERAL CONFIGURATION ##
    @property
    def dataDirectory(self):
        return self.config["GENERAL"]["dataDirectory"]

    @property
    def recipesDirectory(self):
        return '{0}/recipes/'.format(self.dataDirectory)

    @property
    def logDirectory(self):
        return self.config["GENERAL"]["logDirectory"]
        
    @property
    def logFileMaxBytes(self):
        return self.config["GENERAL"]["logFileMaxBytes"]

    @property
    def logFileBackupCount(self):
        return self.config["GENERAL"]["logFileBackupCount"]

    @property
    def logToStderr(self):
        return self.config["GENERAL"]["logToStderr"]

    @property
    def logLevel(self):
        return self.config["GENERAL"]["logLevel"]

    ## FLASK CONFIGURATION ##
    @property
    def apiPort(self):
        return environ.get("API_PORT", self.config["FLASK"]["apiPort"])  

    ## HARDWARE CONFIGURATION ##
    @property
    def hardwareSpeedup(self):
        # Speeds up every task for testing hardware. Should be set to 1 for actual use
        return environ.get("HARDWARE_SPEEDUP", 1)  

    @property
    def controllerHardware(self):
        return self.config["HARDWARE"]["controllerHardware"]

    @controllerHardware.setter
    def controllerHardware(self, value):
        self.config["HARDWARE"]["controllerHardware"] = value
        self.config.write()

    @property
    def hardwareDirectory(self):
        return '{0}/hardware/'.format(self.dataDirectory)

    @property
    def controllerHardwareDirectory(self):
        return '{0}/controllerhardware/'.format(self.hardwareDirectory)

    @property
    def labHardwareDirectory(self):
        return '{0}/labhardware/'.format(self.hardwareDirectory)

    @property
    def labHardware(self):
        return self.config["HARDWARE"]["labHardware"]

    @labHardware.setter
    def labHardware(self, value):
        self.config["HARDWARE"]["labHardware"] = value
        self.config.write()


microlabConfig = MicrolabConfig()


def initialSetup():
    dataDirectory = microlabConfig.dataDirectory
    recipesDirectory = microlabConfig.recipesDirectory
    hardwareDirectory = microlabConfig.hardwareDirectory
    controllerHardwareDirectory = microlabConfig.controllerHardwareDirectory
    labHardwareDirectory = microlabConfig.labHardwareDirectory
    # ensure data directories exist
    makedirs(path.dirname(dataDirectory), exist_ok=True)
    makedirs(path.dirname(recipesDirectory), exist_ok=True)
    makedirs(path.dirname(hardwareDirectory), exist_ok=True)
    makedirs(path.dirname(controllerHardwareDirectory), exist_ok=True)
    makedirs(path.dirname(labHardwareDirectory), exist_ok=True)
  
    # ensure log directory exists
    makedirs(path.dirname(microlabConfig.logDirectory + "/"), exist_ok=True)

    # copy builtin controller configurations to data directory, 
    # overwriting old configurations if they exist
    defaultControllerConfigsDir = "./data/hardware/controllerhardware/"
    for controllerhardware in os.listdir(defaultControllerConfigsDir):
        src = "{0}/{1}".format(defaultControllerConfigsDir, controllerhardware)
        dest = "{0}/{1}".format(controllerHardwareDirectory, controllerhardware)
        shutil.copy2(src, dest)

    # copy builtin lab configurations to data directory,
    # overwriting old configurations if they exist
    defaultLabConfigsDir = "./data/hardware/labhardware/"
    for labhardware in os.listdir(defaultLabConfigsDir):
        src = "{0}/{1}".format(defaultLabConfigsDir, labhardware)
        dest = "{0}/{1}".format(labHardwareDirectory, labhardware)
        shutil.copy2(src, dest)

    # copy builtin recipes to data directory, 
    # overwriting old recipes if they exist
    defaultRecipesDir = "./data/recipes/"
    for recipe in os.listdir(defaultRecipesDir):
        src = "{0}/{1}".format(defaultRecipesDir, recipe)
        dest = "{0}/{1}".format(recipesDirectory, recipe)
        shutil.copy2(src, dest)
