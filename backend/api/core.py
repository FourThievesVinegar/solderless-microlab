"""
Module init.
Contains function for starting up the flask process
"""
import logging

import api.routes
from config import microlabConfig as config
from api.app import app
from microlab.interface import MicrolabInterface


def runFlask(in_queue, out_queue):

    logging.info("### STARTING API ###")
    werkzeugLogger = logging.getLogger("werkzeug")
    # suppresses logging of individual requests to endpoints. Prevents log spam
    werkzeugLogger.setLevel(logging.WARNING)

    api.routes.microlabInterface = MicrolabInterface(in_queue, out_queue)
    app.run(host="0.0.0.0", port=config.apiPort)
