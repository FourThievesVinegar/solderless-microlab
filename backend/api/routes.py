"""
Module defining API.
"""

from api import app
from flask import jsonify, request
from werkzeug.utils import secure_filename
from os.path import join
import recipes
import json


@app.route('/list')
def listRecipes():
    """
    List all available recipes

    :return:
    list
        a list containing the names of the recipes. ex: ['recipe1','recipe2']
    """
    recipeNames = list(map(lambda recipe: recipe['title'], recipes.getRecipeList()))
    return jsonify(recipeNames)


@app.route('/recipe/<name>')
def sendRecipe(name):
    recipe = recipes.getRecipeByName(name)
    return jsonify(recipe)


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
        time
            The number of seconds the current step will execute for
        icon
            String indicating an icon to display to the user or undefined
            if the recipe does not specify an icon for the step.
            One of:
                reaction_complete
                cooling
                crystalisation
                dispensing
                dry
                filter
                heating
                human_task
                inspect
                load_syringe
                maintain_cool
                maintain_heat
                reaction_chamber
                rinse
                set_up_cooling
                set_up_heating
                stirring
                temperature
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

@app.route('/uploadRecipe', methods = ['POST'])
def uploadRecipe():
    """
    Uploads a file to the recipes folder, file must be valid JSON.

    :return:
    object
        response
            One of:
                ok
                error
        message
            Only present if response is "error" and there is a message to present to the user.
    """
    
    f = request.files['File']
    if f.mimetype != 'application/json':
        return jsonify({'response': 'error', 'message': "Recipe is not a json file."}), 400
    try:
        json.load(f.stream)
    except Exception as e:
        return jsonify({'response': 'error', 'message': "File does not contain valid JSON."}), 400
    #reading the stream above sets the stream position to EOF, need to go back to start
    f.stream.seek(0)
    f.save(join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    return jsonify({'response': 'ok'})
