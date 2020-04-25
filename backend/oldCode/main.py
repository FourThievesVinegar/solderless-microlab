from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import relay
import relay_testing

@app.route('/')
def index():
    return '<h1>Hello world!</h1>'

@app.route('/test/relays')
def test_relays():
    relay_test.test_relays()
    return ''

if __name__ == '__main__':
    relay.init_relays()

    app.run(host='0.0.0.0', use_reloader=True)
