import logging
import signal
import sys
from types import FrameType
from typing import Optional

from flask import Flask
from waitress.server import create_server, MultiSocketServer

from config import microlabConfig as config
from localization import load_translation
from microlab.interface import MicrolabInterface
from util.logger import MultiprocessingLogger


class WaitressAPIServer:
    def __init__(self, app: Flask, microlab_interface: MicrolabInterface):
        self.app: Flask = app
        self.server: Optional[MultiSocketServer] = None
        self.logger: logging.Logger = MultiprocessingLogger.get_logger(__name__)
        self.t = load_translation()

        signal.signal(signal.SIGINT, self._shutdown_signal_handler)
        signal.signal(signal.SIGTERM, self._shutdown_signal_handler)
        self.microlab_interface: MicrolabInterface = microlab_interface

    def run(self) -> None:
        self.logger.info(self.t['starting-waitress'])
        self.server = create_server(self.app, host='0.0.0.0', port=config.apiPort)
        self.logger.info(self.t['server-type'].format(type(self.server).__name__))
        self.server.run()

    def _shutdown_signal_handler(self, signum: int, frame: Optional[FrameType]) -> None:
        self.shutdown()

    def shutdown(self) -> None:
        if self.server:
            self.logger.debug(self.t['shutting-waitress'])
            self.server.close()
            self.logger.debug(self.t['shutted-waitress'])
