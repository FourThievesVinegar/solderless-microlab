import logging
import os
import sys
import signal

from abc import ABC, abstractmethod

from waitress.server import create_server
from flask import Flask

from config import microlabConfig as config
from microlab.interface import MicrolabInterface


LOGGER = logging.getLogger(__name__)


class APIServer(ABC):

    _microlab_interface = None

    def __init__(self, app: Flask):
        self._app = app
        # self._microlab_interface = microlab_interface

    @classmethod
    def set_microlab_interface(cls, microlab_interface: MicrolabInterface):
        cls._microlab_interface = microlab_interface

    @abstractmethod
    def run(self):
        raise NotImplementedError('Child classes must implement "run" method.')

    @classmethod
    @abstractmethod
    def shutdown(self):
        raise NotImplementedError('Child classes must implement "shutdown" method.')


class WaitressAPIServer(APIServer):

    _server = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        signal.signal(signal.SIGINT, self._shutdown_signal_handler)
        signal.signal(signal.SIGTERM, self._shutdown_signal_handler)

    def run(self):
        LOGGER.info('Starting backend server')
        # self._server.serve_forever()
        self._get_server(self._app).run()

    def _shutdown_signal_handler(self, signum, frame):
        sys.stdout.write('In WaitressAPIServer signal handler\n')
        sys.stdout.flush()
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
            # LOGGER.info('Shutting down backend server')
            sys.stdout.write('Shutting down backend server\n')
            sys.stdout.flush()
            cls._server.close()
            # LOGGER.info('Shutting down backend server complete')
            sys.stdout.write('Shutting down backend server complete\n')
            sys.stdout.flush()

        sys.stdout.write('Begining purge of toMicrolab queue\n')
        sys.stdout.flush()
        cls._microlab_interface.close_to_microlab_queue()
        sys.stdout.write('Completed purge of toMicrolab queue\n')
        sys.stdout.flush()

        # logging.shutdown()
        sys.stdout.write('Last call before os._exit in flask\n')
        sys.stdout.flush()
        os._exit(os.EX_OK)
