"""
This package is responsible for managing the recipe files and routing the recipe steps
to the appropriate recipe.

The current running recipe is kept in recipes.state.currentRecipe.
The directory the recipes reside is configured in config.recipesPackage. All json files in that
directory should be considered recipes.
"""

import json
from os import listdir
from os.path import isfile, join
from typing import Optional, Any

from pydantic_core import ValidationError

from config import microlab_config as config
from hardware.core import MicroLabHardware, MicroLabHardwareState
from localization import load_translation
from recipes import state
from recipes.base import RunningRecipe
from recipes.model import MicrolabRecipe
from util.logger import MultiprocessingLogger


def get_recipe_list() -> list[MicrolabRecipe]:
    """
    :return:
        A list of modules in the config.recipesPackages.
        It is assumed that these are all recipes.
    """
    t = load_translation()
    logger = MultiprocessingLogger.get_logger(__name__)

    files = [f for f in listdir(config.recipesDirectory) if isfile(join(config.recipesDirectory, f))]
    recipe_list: list[MicrolabRecipe] = []

    for f in files:
        if f.endswith('.json'):
            try:
                with open(join(config.recipesDirectory, f)) as inf:
                    recipe_data = json.load(inf)
                    recipe_data['fileName'] = f
                    recipe_list.append(MicrolabRecipe.model_validate(recipe_data))
            except ValidationError as err:
                logger.error(t['error-recipe-file'].format(f, str(err)))
            except json.JSONDecodeError:
                logger.error(t['error-json-recipe-file'].format(f))

        if f.endswith('.4tv'):
            # FIXME: convert `f` to MicrolabRecipe
            recipe_list.append(f[:-4])

    return recipe_list


def get_recipe_by_name(name: str) -> Optional[MicrolabRecipe]:
    """
    Gets the full recipe object by its name.
    :param name:
        The name of the recipe. This is its title in the json file.
    :return:
        The first recipe object or None if no recipe with given name could be found
    """
    matches = [r for r in get_recipe_list() if r.title == name]
    return matches[0] if matches else None


def start(name: str) -> tuple[bool, str]:
    """
    Start running a recipe.

    A recipe can only be started if the current state of the machine is idle or complete
    and the recipe exists in the list of recipes.
    :param name:
        The name of the recipe. Must be the title of an element of the recipes.list list.
    :return:
        (True, '') on success.
        (False, message) on failure.
    """
    t = load_translation()
    microlab_hardware = MicroLabHardware.get_microlab_hardware_controller()
    if microlab_hardware.state is not MicroLabHardwareState.INITIALIZED:
        return False, t['microlab-failed-start'].format(microlab_hardware.error)

    current = state.current_recipe
    if current and current.get_status().get('status') != 'complete':
        return False, t['stop-recipe-running'].format(current.title)

    recipe = get_recipe_by_name(name)
    if recipe is None:
        return False, t['recipe-unknown']

    state.current_recipe = RunningRecipe(recipe, microlab_hardware)
    state.current_recipe.start()

    return True, ''


def status(*args, **kwargs) -> dict[str, Any]:
    """
    Get the status of the machine.
    :return:
    object
        message
            The message to be displayed to the user.
        options
            null or a list of strings to display to the user as selectable options.
        recipe
            Name of the currently running recipe or null if none is running.
        step
            The step number or -1 if no recipe is running
        status
            The state of the application. One of:
                idle
                    App is waiting for the user to start a recipe
                running
                    App is running a recipe and doesn't need any input from the user
                user_input
                    App is waiting for the user to make a decision. See options.
                complete
                    Recipe is complete.
                error
                    A system error has occurred.
        icon
            The icon to show in the UI. See StatusIcon.jsx for supported icons.
        stepCompletionTime
            An ISO date string for when the current step is expected to be completed,
            or null if unknown. 
    """
    t = load_translation()
    message: dict[str, Any] = {
        'status': 'idle',
        'recipe': None,
        'step': -1,
        'message': None,
        'options': [],
        'stepCompletionTime': None
    }
    microlab_hardware = MicroLabHardware.get_microlab_hardware_controller()
    if microlab_hardware.state is MicroLabHardwareState.FAILED_TO_START:
        message['status'] = t['error']
        message['message'] = t['microlab-failed-to-start']
        message['hardwareError'] = str(microlab_hardware.error)
        return message

    if state.current_recipe is None:
        return message

    recipe_message = state.current_recipe.get_status()
    message['status'] = recipe_message['status']
    message['step'] = recipe_message['step']
    message['recipe'] = state.current_recipe.title
    message['message'] = recipe_message['message']
    message['options'] = recipe_message['options']
    message['icon'] = recipe_message['icon']
    message['stepCompletionTime'] = recipe_message['stepCompletionTime']
    message['temp'] = microlab_hardware.getTemp()
    return message


def stop(*args, **kwargs) -> None:
    """
    Stop the currently running recipe.
    :return:
        None
    """
    if not state.current_recipe is None:
        state.current_recipe.stop()
        state.current_recipe = None


def select_option(option_value: str) -> tuple[bool, str]:
    """
    Pass in the user selected option from a recipe step.

    The current step must have provided a list of options through the /status API
    and the option must be part of the list provided as an option.
    :param option_value:
        The selected option. It must be part of the options list as retrieved via /status
    :return:
        (True, '') on success
        (False, message) on failure
    """
    t = load_translation()
    if not state.current_recipe is None:
        return state.current_recipe.select_option(option_value)
    return False, t['no-running-recipe']
