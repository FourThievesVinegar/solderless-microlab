"""
Module defining API.
"""

from api import app
from flask import jsonify
import recipes


@app.route('/list')
def list():
    """
    List all available recipes

    :return:
    list
        a list containing the names of the recipes. ex: ['recipe1','recipe2']
    """
    recipes.refresh()
    return jsonify(recipes.list)


@app.route('/recipe/<name>')
def sendRecipe(name):
    recipe = __import__("recipes.files." + name, globals(), locals(), name)
    return jsonify(recipe.recipe.plan)


@app.route('/status')
def status():
    """
    Get the status of the app.

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
    return jsonify(recipes.status())


@app.route('/start/<name>')
def start(name):
    """
    Start running a recipe.

    :param name:
        The recipe name. Must be one of the items returned by /list
    :return:
    object
        response
            One of:
                ok
                error
        message
            Only present if response is "error" and there is a message to present to the user.
    """
    (state, msg) = recipes.start(name)
    if state:
        return jsonify({'response': 'ok'})
    else:
        return jsonify({'response': 'error', 'message': msg})


@app.route('/stop')
def stop():
    """
    Stop the currently running recipe.

    :return:
    object
        response
            One of:
                ok
                error
        message
            Only present if response is "error" and there is a message to present to the user.
    """
    recipes.stop()
    return jsonify({'response': 'ok'})


@app.route('/select/option/<name>')
def selectOption(name):
    """
    Provide user selected input.

    :param name:
    The name of the user selected option. This must be one of the strings presented in the
    "options" list in the /status call.

    :return:
    object
        response
            One of:
                ok
                error
        message
            Only present if response is "error" and there is a message to present to the user.
    """
    (state, msg) = recipes.selectOption(name)
    if state:
        return jsonify({'response': 'ok'})
    else:
        return jsonify({'response': 'error', 'message': msg})
