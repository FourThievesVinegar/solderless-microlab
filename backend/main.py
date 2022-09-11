# Start the application on the default port (5000)
# Look in api.routes for the actual api code

from api import app
import config

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, use_reloader=True)
