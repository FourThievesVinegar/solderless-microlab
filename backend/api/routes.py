"""
Module defining API.
"""

# from api.app import get_flask_app
from api.server import APIServer
from flask import Flask
from flask import jsonify, request, send_file
from werkzeug.utils import secure_filename
from os.path import join
import os
import recipes.core
import json
from config import microlabConfig as config
import glob 
from pathlib import Path

from microlab.interface import MicrolabInterface

# self._microlab_interface = None

# APP = get_flask_app()


class RouteManager:

    def __init__(self, flask_app: Flask, microlab_interface: MicrolabInterface):
        self._flask_app = flask_app
        self._microlab_interface = microlab_interface
        self._register_routes()

    # @app.route('/list') X
    def _list_recipes(self):
        """
        List all available recipes

        :return:
        list
            a list containing the names of the recipes. ex: ['recipe1','recipe2']
        """
        recipeNames = list(map(lambda recipe: recipe['title'], recipes.core.getRecipeList()))
        return jsonify(recipeNames)

    # @app.route('/recipe/<name>') X
    def _send_recipe(self, name):
        recipe = recipes.core.getRecipeByName(name)
        return jsonify(recipe)

    # @app.route('/status') X
    def _status(self):
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
        return jsonify(self._microlab_interface.status())

    # @app.route('/start/<name>', methods=['POST']) X
    def _start(self, name):
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
        if recipe is None:
            return jsonify(
                {
                    'response': 'error', 'message': 'Recipe with this name could not be found'
                }
            ), 404
                            
        (state, msg) = self._microlab_interface.start(name)
        if state:
            return jsonify({'response': 'ok'})
        else:
            return jsonify({'response': 'error', 'message': msg}), 500

    # @app.route('/stop', methods=['POST']) X
    def _stop(self):
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
        self._microlab_interface.stop()
        return jsonify({'response': 'ok'})

    # @app.route('/select/option/<name>', methods=['POST']) X
    def _select_option(self, name):
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
        (state, msg) = self._microlab_interface.selectOption(name)
        if state:
            return jsonify({'response': 'ok'})
        else:
            return jsonify({'response': 'error', 'message': msg}), 400

    # @app.route('/uploadRecipe', methods = ['POST']) X
    def _upload_recipe(self):
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

    # @app.route('/controllerHardware') X
    def _get_controller_hardware(self):
        """
        Gets the current controller hardware setting

        :return:
        object
            controllerHardware
                A string with the current controller hardware setting
        """
        return (jsonify({'controllerHardware': config.controllerHardware}), 200)

    # @app.route('/controllerHardware/list') X
    def _list_controller_hardware(self):
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

    # @app.route('/controllerHardware/<name>', methods=['POST']) X
    def _select_controller_hardware(self, name):
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
        self._microlab_interface.reloadConfig()
        (success, msg) = self._microlab_interface.reloadHardware()
        if success:
            return (jsonify({'response': 'ok'}), 200)
        else:
            return jsonify({'response': 'error', 'message': msg}), 400

    # @app.route('/uploadControllerConfig', methods = ['POST']) X
    def _upload_controller_config(self):
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

    # @app.route('/downloadControllerConfig/<name>') X
    def _download_controller_config(self, name):
        """
        Downloads a controller hardware configuration file

        :return:
        The controller configuration file
        """
        fileName = "{0}.yaml".format(secure_filename(name))
        return send_file(join(config.controllerHardwareDirectory, fileName), name, as_attachment=True)

    # @app.route('/labHardware') X
    def _get_lab_hardware(self):
        """
        Gets the current lab hardware setting

        :return:
        object
            labHardware
                A string with the current lab hardware setting
        """
        return (jsonify({'labHardware': config.labHardware}), 200)

    # @app.route('/labHardware/list') X
    def _list_lab_hardware(self):
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

    # @app.route('/labHardware/<name>', methods=['POST']) X
    def _select_lab_hardware(self, name):
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
        self._microlab_interface.reloadConfig()
        (success, msg) = self._microlab_interface.reloadHardware()
        if success:
            return (jsonify({'response': 'ok'}), 200)
        else:
            return jsonify({'response': 'error', 'message': msg}), 400

    # @app.route('/uploadLabConfig', methods = ['POST']) X
    def _upload_lab_config(self):
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

    # @app.route('/downloadLabConfig/<name>')
    def _download_lab_config(self, name):
        """
        Downloads a lab hardware configuration file

        :return:
        The lab configuration file
        """
        fileName = "{0}.yaml".format(secure_filename(name))
        return send_file(join(config.labHardwareDirectory, fileName), name, as_attachment=True)

    # @app.route('/reloadHardware', methods=['POST']) X
    def _reload_hardware(self):
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
        self._microlab_interface.reloadConfig()
        (success, msg) = self._microlab_interface.reloadHardware()
        if success:
            return (jsonify({'response': 'ok'}), 200)
        else:
            return jsonify({'response': 'error', 'message': msg}), 400

    # @app.route('/log') X
    def _fetch_logs(self):
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

    # @app.route('/shutdown', methods=['PUT']) X
    def _shutdown_server(self):
        """Stops server """
        # At first read this seems excessive to kill the server however after
        # digging deeper into it this may be the cleanest way to deal with this.
        print('Hit shutdown endpoint')
        print('Calling server shutdown now')
        APIServer.shutdown()

        # try:
        #     return (jsonify({'response': 'ok'}), 200)
        # finally:
        #     print('Calling server shutdown now')
        #     APIServer.shutdown()

    def _register_routes(self):
        # def add_api_route(self, rule: str, endpoint_function: Callable, methods: Optional[list[str]] = None):

        # recipes
        self._flask_app.add_api_route('/list', self._list_recipes)
        self._flask_app.add_api_route('/recipe/<name>', self._send_recipe)
        self._flask_app.add_api_route('/uploadRecipe', self._upload_recipe, ['POST'])

        # flow control
        self._flask_app.add_api_route('/start/<name>', self._start, ['POST'])
        self._flask_app.add_api_route('/stop', self._stop, ['POST'])
        self._flask_app.add_api_route('/select/option/<name>', self._select_option, ['POST'])

        # controller hardware
        self._flask_app.add_api_route('/controllerHardware', self._get_controller_hardware)
        self._flask_app.add_api_route('/controllerHardware/list', self._list_controller_hardware)
        self._flask_app.add_api_route('/controllerHardware/<name>', self._select_controller_hardware, ['POST'])
        self._flask_app.add_api_route('/uploadControllerConfig', self._upload_controller_config, ['POST'])
        self._flask_app.add_api_route('/downloadControllerConfig/<name>', self._download_controller_config)

        # lab hardware
        self._flask_app.add_api_route('/labHardware', self._get_lab_hardware)
        self._flask_app.add_api_route('/labHardware/list', self._list_lab_hardware)
        self._flask_app.add_api_route('/labHardware/<name>', self._select_lab_hardware, ['POST'])
        self._flask_app.add_api_route('/uploadLabConfig', self._upload_lab_config, ['POST'])
        self._flask_app.add_api_route('/downloadLabConfig/<name>', self._download_lab_config)
        self._flask_app.add_api_route('/reloadHardware', self._reload_hardware, ['POST'])

        # utils
        self._flask_app.add_api_route('/status', self._status)
        self._flask_app.add_api_route('/log', self._fetch_logs)
        self._flask_app.add_api_route('/shutdown', self._shutdown_server, ['PUT'])
