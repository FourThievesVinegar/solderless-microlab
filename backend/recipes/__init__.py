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
from recipes import state
from recipes.base import Recipe
from hardware import microlabHardware, MicroLabHardwareState
from config import microlabConfig as config 
import logging

def getRecipeList():
    """
    :return:
    A list of modules in the config.recipesPackages.
    It is assumed that these are all recipes.
    """
    path = config.recipesDirectory
    files = [f for f in listdir(path) if isfile(join(path, f))]
    recipeList = []

    for f in files:
        if f.endswith('.json'):
            try:
                recipeList.append(json.load(open(join(path, f))))
            except json.JSONDecodeError:
                logging.error("Error loading recipe file: {0}. File is not in proper JSON format".format(f))
        # This doesn't actually work yet because .4tv are not importable as modules
        if f.endswith('.4tv'):
            recipeList.append(f[:-4])

    return recipeList

def getRecipeByName(name):
    """
    Gets the full recipe object from its name.
    :param name:
    The name of the recipe. This is its title in the json file.
    :return:
    The recipe object or None if no recipe with given name could be found
    """
    recipeList = getRecipeList()

    recipe = next(filter(lambda recipe: recipe['title'] == name, recipeList), None)

    return recipe

def start(name):
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
    # Validate that the microlab hardware controller has initialized
    if microlabHardware.state is not MicroLabHardwareState.INITIALIZED:
        return False, 'Microlab failed to start. Check Hardware configuration and setup'.format(microlabHardware.error)

    # If we are currently running a recipe, check if it is complete.
    if not (state.currentRecipe is None):
        recipeMessage = state.currentRecipe.getStatus()
        if not recipeMessage['status'] == 'complete':
            return False, 'Recipe {0} is running. Stop it first.'.format(state.currentRecipe.plan['title'])

    # Check that it's a valid recipe.
    recipe = getRecipeByName(name)
    if recipe is None:
        return False, 'Recipe unknown.'

    # Start running the recipe
    state.currentRecipe = Recipe(recipe)

    state.currentRecipe.start()

    return True, ''


def status(_):
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
    message = {
        'status': 'idle',
        'recipe': None,
        'step': -1,
        'message': None,
        'options': [],
        'stepCompletionTime': None
    }
    if microlabHardware.state is MicroLabHardwareState.FAILED_TO_START:
        message['status'] = 'error'
        message['message'] = 'Microlab failed to start. Check hardware and configuration'
        return message

    if state.currentRecipe == None:
        return message

    recipeMessage = state.currentRecipe.getStatus()
    message['status'] = recipeMessage['status']
    message['step'] = recipeMessage['step']
    message['recipe'] = state.currentRecipe.plan['title']
    message['message'] = recipeMessage['message']
    message['options'] = recipeMessage['options']
    message['icon'] = recipeMessage['icon']
    message['stepCompletionTime'] = recipeMessage['stepCompletionTime']
    message['temp'] = microlabHardware.getTemp()

    return message


def stop(_):
    """
    Stop the currently running recipe.

    :return:
    None ... at least for now.
    """

    if not state.currentRecipe is None:
        state.currentRecipe.stop()
        state.currentRecipe = None


def selectOption(option):
    """
    Pass in the user selected option from a recipe step.

    The current step must have provided a list of options through the /status API
    and the option must be part of the list provided as an option.
    :param option:
    The selected option. It must be part of the options list as retrieved via /status
    :return:
    (True, '') on success
    (False, message) on failure
    """
    if not state.currentRecipe is None:
        return state.currentRecipe.selectOption(option)
    return False, 'No recipe running.'
