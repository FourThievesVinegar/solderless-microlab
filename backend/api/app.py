"""
Initializing the app and adding a CORS header to all the API calls.
"""

from flask import Flask
from flask_cors import CORS
import config

app = Flask(__name__)
CORS(app)

from api import routes