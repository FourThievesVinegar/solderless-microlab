# Start the application on the configured port (default 8081)
# Look in api.routes for the actual api code
from os import environ
from api import app
import config

reload = False if environ.get("FLASK_ENV") == 'production' else True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.apiPort, use_reloader=reload)
