import logging
import os
import sys

from abc import ABC, abstractmethod

from waitress.server import create_server
from flask import Flask

from config import microlabConfig as config
from microlab.interface import MicrolabInterface


LOGGER = logging.getLogger(__name__)


class APIServer(ABC):

    def __init__(self, app: Flask, microlab_interface: MicrolabInterface):
        self._app = app
        self._microlab_interface = microlab_interface

    @abstractmethod
    def run(self):
        raise NotImplementedError('Child classes must implement "run" method.')

    @abstractmethod
    def shutdown(self):
        raise NotImplementedError('Child classes must implement "shutdown" method.')


class WaitressAPIServer(APIServer):

    _server = None

    # def __init__(self, app: Flask):
    #     self._app = app

    def run(self):
        LOGGER.info('Starting backend server')
        # self._server.serve_forever()
        self._get_server(self._app).run()

    @classmethod
    def _get_server(cls, app: Flask):
        if cls._server is None:
            cls._server = create_server(app, host='0.0.0.0', port=config.apiPort)
        return cls._server

    def shutdown(self):
        LOGGER.info('Shutting down backend server')
        self._server.close()
        LOGGER.info('Shutting down backend server complete')

        sys.stdout.write('Begining purge of toMicrolab queue\n')
        sys.stdout.flush()
        self._microlab_interface.close_to_microlab_queue()
        sys.stdout.write('Completed purge of toMicrolab queue\n')
        sys.stdout.flush()

        # logging.shutdown()
        sys.stdout.write('Last call before os._exit in flask\n')
        sys.stdout.flush()
        os._exit(os.EX_OK)
