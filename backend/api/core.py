"""
Module init.
Contains function for starting up the flask process
"""
from multiprocessing import Queue

from api.routes import RouteManager
from api.server import WaitressAPIServer
from api.app import FlaskApp
from microlab.interface import MicrolabInterface
from util.logger import MultiprocessingLogger
from localization import load_translation

def start_flask_process(cmd_queue: Queue, resp_queue: Queue, logging_queue: Queue) -> None:
    # The initialize_logger call only needs to happen once when a new process is started.
    MultiprocessingLogger.initialize_logger(logging_queue)
    logger = MultiprocessingLogger.get_logger(__name__)
    
    t = load_translation()
    logger.info(t['starting-api'])

    microlab_interface = MicrolabInterface(cmd_queue, resp_queue)

    flask_app = FlaskApp()

    # This handles the routes and registering them to the flask_app instance
    RouteManager(flask_app, microlab_interface)

    server = WaitressAPIServer(flask_app.get_flask_app(), microlab_interface)
    server.run()
