"""
This package is responsible for managing the recipe files and routing the recipe steps
to the appropriate recipe.

The current running recipe is kept in recipes.state.currentRecipe. The reason this is in its own
module is to avoid circular references as this module needs to import recipes.celery and
recipes.celery needs to import the currentRecipe.

The idea here is that the currentRecipe represents the module name of the recipe. Each recipe
implements a standard interface defined in recipes.base. This module then routes the requests
from the API to appropriate package by simply importing the appropriate package at runtime.

The directory the recipes reside is configured in config.recipesPackage. All modules in that
directory should be considered recipes.
"""

from os import listdir
from os.path import isfile, join
from recipes import state


# Not used for now. Recipe list hardcoded below
def getList():
    """
    Not currently used. The list of recipes is currently hardcoded.
    This method works and the code should work with it but due to possible bugs
    from the dynamic nature of this method it has been decided to hardcode the
    recipes for now.
    :return:
    A list of modules in the config.recipesPackages.
    It is assumed that these are all recipes.
    """
    path = './' + state.package.replace('.', '/')
    files = [f for f in listdir(path) if isfile(join(path, f))]
    list = []

    for f in files:
        if not f.startswith('__init__'):
            if f.endswith('.py'):
                list.append(f[:-3])

    return list


#list = getList()
# Hardcoded list of recipes.
list = ['boilegg']

def refresh():
    """
    Not currently used. Refreshes the dynamic list of recipes at runtime.
    This would allow recipes to be downloaded and imported at runtime.
    :return:
    """
    global list
    #list = getList()


def start(name):
    """
    Start running a recipe.

    A recipe can only be started if the current state of the machine is idle or complete
    and the recipe exists in the list of recipes.
    :param name:
    The name of the recipe. This must be part of recipes.list list.
    :return:
    (True, '') on success.
    (False, message) on failure.
    """
    global list

    # If we are currently running a recipe, check if it is complete.
    if not (state.currentRecipe is None):
        # Dynamically import the recipe based on the name in status.currentRecipe.
        exec('from ' + state.package + '.' + state.currentRecipe + ' import recipe')
        # Need to use eval to be able to make the call to the dynamically imported recipe.
        recipeMessage = eval('recipe.getStatus()')
        if not recipeMessage['status'] == 'complete':
            return False,'Recipe ' + state.currentRecipe + ' is running. Stop it first.'

    # Check that it's a valid recipe.
    if not (name in list):
        return False,'Recipe unknown.'

    # Start running the recipe
    state.currentRecipe = name
    exec('from ' + state.package + '.' + state.currentRecipe + ' import recipe')
    currentStep = eval('recipe.start()')

    return True,''


def status():
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
    """
    message = {
        'status':'idle',
        'recipe':state.currentRecipe,
        'step':-1,
        'message':None,
        'options':[]
    }

    if state.currentRecipe == None:
        return message

    # Dynamically import the recipe based on the name in status.currentRecipe.
    exec('from ' + state.package + '.' + state.currentRecipe + ' import recipe')
    # Need to use eval to be able to make the call to the dynamically imported recipe.
    recipeMessage = eval('recipe.updateStatus()')
    message['status'] = recipeMessage['status']
    message['step'] = recipeMessage['step']
    message['message'] = recipeMessage['message']
    message['options'] = recipeMessage['options']

    return message


def stop():
    """
    Stop the currently running recipe.

    TODO: Implement mechanism for stopping associated celery tasks
    :return:
    None ... at least for now.
    """

    if not state.currentRecipe is None:
        exec('from ' + state.package + '.' + state.currentRecipe + ' import recipe')
        exec('recipe.stop()')
        state.currentRecipe = None


def selectOption(option):
    """
    Pass in the use selected option from a recipe step.

    The current step must have provided a list of options through the /status API
    and the option must be part of the list provided as an option.
    :param option:
    The selected option. It must be part of the options list as retrived via /status
    :return:
    (True,'') on success
    (False,message) on failure
    """
    if not state.currentRecipe is None:
        exec('from ' + state.package + '.' + state.currentRecipe + ' import recipe')
        return eval('recipe.selectOption(option)')
    return False,'No recipe running.'
