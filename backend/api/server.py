import logging
import sys
import signal

from waitress.server import create_server
from flask import Flask

from config import microlabConfig as config
from microlab.interface import MicrolabInterface


LOGGER = logging.getLogger(__name__)


class WaitressAPIServer:

    _server = None
    _microlab_interface = None

    def __init__(self, app: Flask):
        self._app = app
        signal.signal(signal.SIGINT, self._shutdown_signal_handler)
        signal.signal(signal.SIGTERM, self._shutdown_signal_handler)

    @classmethod
    def set_microlab_interface(cls, microlab_interface: MicrolabInterface):
        cls._microlab_interface = microlab_interface

    def run(self):
        LOGGER.info('Starting backend waitress server')
        self._get_server(self._app).run()

    def _shutdown_signal_handler(self, signum, frame):
        self.shutdown()

    @classmethod
    def _get_server(cls, app: Flask):
        if cls._server is None:
            cls._server = create_server(app, host='0.0.0.0', port=config.apiPort)
            print(f'server type: {type(cls._server).__name__}')
        return cls._server

    @classmethod
    def shutdown(cls):
        if cls._server:
            LOGGER.debug('Shutting down waitress server')
            cls._server.close()
            LOGGER.debug('Completed shut down of waitress server')

        cls._microlab_interface.close_to_microlab_queue()

        sys.exit(0)
