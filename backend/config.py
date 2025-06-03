"""
This file contains an interface for configuration loaded from and written to
disk and/or passed in as environment variables. Import and use this file with
"from config import microlabConfig as config"
Configuration is stored on disk at '/etc/microlab/microlab.ini'
"""
import logging
import shutil
from os import environ, makedirs, path, listdir

from configobj import ConfigObj, flatten_errors
from configobj.validate import Validator

MICROLAB_CONFIG_DIR = environ.get('MICROLAB_CONFIG_DIR', '/etc/microlab/')
BACKEND_DIR = path.dirname(path.abspath(__file__))


class MicrolabConfig:
    """
    Contains all the microlab configuration values fetched from disk. Uses a
    class to abstract away setters to write to disk, and ability to reload
    changes from disk.
    """
    def __init__(self):
        fqfp_microlab_ini = path.join(MICROLAB_CONFIG_DIR, 'microlab.ini')
        self.config = ConfigObj(fqfp_microlab_ini, configspec=path.join(BACKEND_DIR, 'defaultconfig.ini'))

    def validate_config(self) -> None:
        validator = Validator()
        validation_data = self.config.validate(validator, copy=True, preserve_errors=True)
        self.config.write()

        for entry in flatten_errors(self.config, validation_data):
            section_list, key, error = entry
            partial_key = self.config
            for section in section_list:
                partial_key = partial_key[section]
                default = partial_key.restore_default(key)

                if key is not None:
                    section_list.append(key)
                else:
                    section_list.append('[missing section]')
                section_string = '.'.join(section_list)
                if error is False:
                    error = 'Missing value or section.'
                logging.warning(
                    f"Configuration error at {section_string}: '{error}', falling back to default value '{default}'."
                )

    def reload_config(self) -> None:
        """ Reloads microlab configuration from disk. """
        self.config.reload()

    ## GENERAL CONFIGURATION ##
    @property
    def dataDirectory(self) -> str:
        return path.join(self.config['GENERAL']['dataDirectory'], '')

    @property
    def recipesDirectory(self) -> str:
        return path.join(self.dataDirectory, 'recipes', '')

    @property
    def logDirectory(self) -> str:
        return path.join(self.config['GENERAL']['logDirectory'], '')

    @property
    def logFileMaxBytes(self) -> int:
        return self.config['GENERAL']['logFileMaxBytes']

    @property
    def logFileBackupCount(self) -> int:
        return self.config['GENERAL']['logFileBackupCount']

    @property
    def logToStderr(self) -> bool:
        return self.config['GENERAL']['logToStderr']

    @property
    def logLevel(self) -> str:
        return self.config['GENERAL']['logLevel']

    ## FLASK CONFIGURATION ##
    @property
    def apiPort(self) -> str:
        return environ.get('API_PORT', self.config['FLASK']['apiPort'])

    ## HARDWARE CONFIGURATION ##
    @property
    def hardwareSpeedup(self) -> int:
        # Speeds up every task for testing hardware. Should be set to 1 for actual use
        return int(environ.get('HARDWARE_SPEEDUP', '1'))

    @property
    def controllerHardware(self) -> str:
        return self.config['HARDWARE']['controllerHardware']

    @controllerHardware.setter
    def controllerHardware(self, value) -> None:
        self.config['HARDWARE']['controllerHardware'] = value
        self.config.write()

    @property
    def hardwareDirectory(self) -> str:
        return path.join(self.dataDirectory, 'hardware', '')

    @property
    def controllerHardwareDirectory(self) -> str:
        return path.join(self.hardwareDirectory, 'controllerhardware', '')

    @property
    def labHardwareDirectory(self) -> str:
        return path.join(self.hardwareDirectory, 'labhardware', '')

    @property
    def labHardware(self) -> str:
        return self.config['HARDWARE']['labHardware']

    @labHardware.setter
    def labHardware(self, value) -> None:
        self.config['HARDWARE']['labHardware'] = value
        self.config.write()


microlab_config = MicrolabConfig()


def initial_setup() -> None:
    # ensure data directories exist
    makedirs(path.dirname(microlab_config.dataDirectory), exist_ok=True)
    makedirs(path.dirname(microlab_config.recipesDirectory), exist_ok=True)
    makedirs(path.dirname(microlab_config.hardwareDirectory), exist_ok=True)
    makedirs(path.dirname(microlab_config.controllerHardwareDirectory), exist_ok=True)
    makedirs(path.dirname(microlab_config.labHardwareDirectory), exist_ok=True)

    # ensure log directory exists
    makedirs(path.dirname(microlab_config.logDirectory), exist_ok=True)

    # copy builtin controller configurations to data directory,
    # overwriting old configurations if they exist
    fqfp_default_controller_dir = path.join(BACKEND_DIR, 'data', 'hardware', 'controllerhardware', '')
    for controllerhardware in listdir(fqfp_default_controller_dir):
        src = path.join(fqfp_default_controller_dir, controllerhardware)
        dest = path.join(microlab_config.controllerHardwareDirectory, controllerhardware)
        shutil.copy2(src, dest)

    # copy builtin lab configurations to data directory,
    # overwriting old configurations if they exist
    fqfp_default_lab_dir = path.join(BACKEND_DIR, 'data', 'hardware', 'labhardware', '')
    for labhardware in listdir(fqfp_default_lab_dir):
        src = path.join(fqfp_default_lab_dir, labhardware)
        dest = path.join(microlab_config.labHardwareDirectory, labhardware)
        shutil.copy2(src, dest)

    # copy builtin recipes to data directory,
    # overwriting old recipes if they exist
    fqfp_default_recipes_dir = path.join(BACKEND_DIR, 'data', 'recipes', '')
    for recipe in listdir(fqfp_default_recipes_dir):
        src = path.join(fqfp_default_recipes_dir, recipe)
        dest = path.join(microlab_config.recipesDirectory, recipe)
        shutil.copy2(src, dest)
