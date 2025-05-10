import logging
import signal
import sys

from flask import Flask
from waitress.server import create_server, MultiSocketServer

from config import microlabConfig as config
from localization import load_translation
from microlab.interface import MicrolabInterface
from util.logger import MultiprocessingLogger


class WaitressAPIServer:
    _server = None
    _microlab_interface = None

    _logger = None

    def __init__(self, app: Flask):
        self._app = app
        signal.signal(signal.SIGINT, self._shutdown_signal_handler)
        signal.signal(signal.SIGTERM, self._shutdown_signal_handler)

        if self._logger is None:
            self._logger = self._get_logger()

    @classmethod
    def _get_logger(cls) -> logging.Logger:
        return MultiprocessingLogger.get_logger(__name__)

    @classmethod
    def set_microlab_interface(cls, microlab_interface: MicrolabInterface) -> None:
        cls._microlab_interface = microlab_interface

    def run(self) -> None:
        t = load_translation()
        self._logger.info(t['starting-waitress'])
        self._get_server(self._app).run()

    def _shutdown_signal_handler(self, signum, frame) -> None:
        self.shutdown()

    @classmethod
    def _get_server(cls, app: Flask) -> MultiSocketServer:
        t = load_translation()
        if cls._server is None:
            cls._server = create_server(app, host='0.0.0.0', port=config.apiPort)
            print(t['server-type'].format(type(cls._server).__name__))
        return cls._server

    @classmethod
    def shutdown(cls) -> None:
        t = load_translation()
        if cls._logger is None:
            cls._logger = cls._get_logger()

        if cls._server:
            cls._logger.debug(t['shutting-waitress'])
            cls._server.close()
            cls._logger.debug(t['shutted-waitress'])

        cls._microlab_interface.close_to_microlab_queue()

        sys.exit(0)
