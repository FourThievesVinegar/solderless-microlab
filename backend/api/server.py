import logging

from waitress.server import create_server
from flask import Flask

from config import microlabConfig as config


class APIServer:

    _server = None

    def __init__(self, app: Flask):
        # self._server = make_server('0.0.0.0', config.apiPort, app)
        self._app = app
        # self.get_server(app)
        # ctx = app.app_context()
        # ctx.push()

    def run(self):
        logging.info('Starting backend server')
        # self._server.serve_forever()
        self.get_server(self._app).run()

    @classmethod
    def get_server(cls, app: Flask):
        if cls._server is None:
            cls._server = create_server(app, host='0.0.0.0', port=config.apiPort)
        return cls._server

    @classmethod
    def shutdown(cls):
        logging.info('Shutting down backend server')
        cls._server.close()
        logging.info('Shutting down backend server complete')
