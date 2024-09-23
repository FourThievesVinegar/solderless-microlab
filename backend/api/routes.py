"""
Module defining API.
"""

from api.app import app
from flask import jsonify, request, send_file
from werkzeug.utils import secure_filename
from os.path import join
import os
import recipes.core
import json
from config import microlabConfig as config
import glob 
from pathlib import Path

microlabInterface = None


@app.route('/list')
def listRecipes():
    """
    List all available recipes

    :return:
    list
        a list containing the names of the recipes. ex: ['recipe1','recipe2']
    """
    recipeNames = list(map(lambda recipe: recipe['title'], recipes.core.getRecipeList()))
    return jsonify(recipeNames)


@app.route('/recipe/<name>')
def sendRecipe(name):
    recipe = recipes.core.getRecipeByName(name)
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
    return jsonify(microlabInterface.status())


@app.route('/start/<name>', methods=['POST'])
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
    recipe = recipes.core.getRecipeByName(name)
    if recipe == None:
        return jsonify({'response': 'error', 
                        'message': 'Recipe with this name could not be found'}
                        ), 404
                        
    (state, msg) = microlabInterface.start(name)
    if state:
        return jsonify({'response': 'ok'})
    else:
        return jsonify({'response': 'error', 'message': msg}), 500


@app.route('/stop', methods=['POST'])
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
    microlabInterface.stop()
    return jsonify({'response': 'ok'})


@app.route('/select/option/<name>', methods=['POST'])
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
    (state, msg) = microlabInterface.selectOption(name)
    if state:
        return jsonify({'response': 'ok'})
    else:
        return jsonify({'response': 'error', 'message': msg}), 400

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
    f.save(join(config.recipesDirectory, secure_filename(f.filename)))
    return jsonify({'response': 'ok'})

@app.route('/controllerHardware')
def getControllerHardware():
    """
    Gets the current controller hardware setting

    :return:
    object
        controllerHardware
            A string with the current controller hardware setting
    """
    return (jsonify({'controllerHardware': config.controllerHardware}), 200)

@app.route('/controllerHardware/list')
def listControllerHardware():
    """
    Gets a list of valid controller hardware settings

    :return:
    list
        a list containing the names of valid controller hardware settings.
        ex: ['pi','AML-S905X-CC-V1.0A']
    """
    files = [recipe for recipe in os.listdir(config.controllerHardwareDirectory)]
    configs = list(map(lambda x: x[:-5], filter(lambda x: x.endswith(".yaml"), files)))
    return jsonify(configs)

@app.route('/controllerHardware/<name>', methods=['POST'])
def selectControllerHardware(name):
    """
    Sets a new controller hardware setting, and reloads the hardware
    controller to use this

    :return:
    object
        response
            One of:
                ok
                error
        message
            Only present if response is "error" and there is a message to present to the user.
    """
    config.controllerHardware = name
    microlabInterface.reloadConfig()
    (success, msg) = microlabInterface.reloadHardware()
    if success:
        return (jsonify({'response': 'ok'}), 200)
    else:
        return jsonify({'response': 'error', 'message': msg}), 400

@app.route('/uploadControllerConfig', methods = ['POST'])
def uploadControllerConfig():
    """
    Uploads a controller hardware configuration file

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
    f.save(join(config.controllerHardwareDirectory, secure_filename(f.filename)))
    return jsonify({'response': 'ok'})

@app.route('/downloadControllerConfig/<name>')
def downloadControllerConfig(name):
    """
    Downloads a controller hardware configuration file

    :return:
    The controller configuration file
    """
    fileName = "{0}.yaml".format(secure_filename(name))
    return send_file(join(config.controllerHardwareDirectory, fileName), name, as_attachment=True)


@app.route('/labHardware')
def getLabHardware():
    """
    Gets the current lab hardware setting

    :return:
    object
        labHardware
            A string with the current lab hardware setting
    """
    return (jsonify({'labHardware': config.labHardware}), 200)

@app.route('/labHardware/list')
def listLabHardware():
    """
    Gets a list of valid lab hardware settings

    :return:
    list
        a list containing the names of valid lab hardware settings.
        ex: ['base_hardware']
    """
    files = [recipe for recipe in os.listdir(config.labHardwareDirectory)]
    configs = list(map(lambda x: x[:-5], filter(lambda x: x.endswith(".yaml"), files)))
    return jsonify(configs)

@app.route('/labHardware/<name>', methods=['POST'])
def selectLabHardware(name):
    """
    Sets a new lab hardware setting, and reloads the hardware
    controller to use this

    :return:
    object
        response
            One of:
                ok
                error
        message
            Only present if response is "error" and there is a message to present to the user.
    """
    config.labHardware = name
    microlabInterface.reloadConfig()
    (success, msg) = microlabInterface.reloadHardware()
    if success:
        return (jsonify({'response': 'ok'}), 200)
    else:
        return jsonify({'response': 'error', 'message': msg}), 400

@app.route('/uploadLabConfig', methods = ['POST'])
def uploadLabConfig():
    """
    Uploads a lab hardware configuration file

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
    f.save(join(config.labHardwareDirectory, secure_filename(f.filename)))
    return jsonify({'response': 'ok'})

@app.route('/downloadLabConfig/<name>')
def downloadLabConfig(name):
    """
    Downloads a lab hardware configuration file

    :return:
    The lab configuration file
    """
    fileName = "{0}.yaml".format(secure_filename(name))
    return send_file(join(config.labHardwareDirectory, fileName), name, as_attachment=True)

@app.route('/reloadHardware', methods=['POST'])
def reloadHardware():
    """
    Reloads the hardware controller

    :return:
    object
        response
            One of:
                ok
                error
        message
            Only present if response is "error" and there is a message to present to the user.
    """
    microlabInterface.reloadConfig()
    (success, msg) = microlabInterface.reloadHardware()
    if success:
        return (jsonify({'response': 'ok'}), 200)
    else:
        return jsonify({'response': 'error', 'message': msg}), 400

@app.route('/log')
def fetchLogs():
    """
    Fetches and concatenates the two most recent microlab log files

    :return:
    object
        logs
            The complete log files as a string
    """
    logFolder = config.logDirectory + "/"
    logFiles = [file for file in glob.glob(os.path.join(logFolder, 'microlab.log*'))]
    print(logFiles)
    logFiles.sort(key=os.path.getmtime)
    data = ""
    if len(logFiles) > 1 and logFiles[-2]:
        data = Path(logFiles[-2]).read_text()
    mostRecent = logFiles[-1]
    data = data + Path(mostRecent).read_text()
    return (jsonify({'logs': data}), 200)
