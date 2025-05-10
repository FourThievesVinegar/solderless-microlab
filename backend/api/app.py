"""
Initializing the app and adding a CORS header to all the API calls.
"""

from flask import Flask
from flask_cors import CORS

from typing import Callable, Optional


class FlaskApp:

    _flask_app = None

    def get_flask_app(self) -> Flask:
        if self._flask_app is None:
            self._flask_app = Flask(__name__)
            CORS(self._flask_app)

        return self._flask_app

    def add_api_route(self, rule: str, endpoint_function: Callable, methods: Optional[list[str]] = None) -> None:
        flask_app = self.get_flask_app()

        if methods:
            flask_app.add_url_rule(rule, view_func=endpoint_function, methods=methods)
        else:
            flask_app.add_url_rule(rule, view_func=endpoint_function)
