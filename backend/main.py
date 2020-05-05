from api import app
import config

if __name__ == '__main__':
    app.run(host='0.0.0.0', use_reloader=True)
