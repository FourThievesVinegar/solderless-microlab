# Start the application on the configured port (default 8081)
# Look in api.routes for the actual api code

from api import app
import config

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.apiPort, use_reloader=True)
