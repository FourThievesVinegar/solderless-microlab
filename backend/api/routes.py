from api import app
from flask import jsonify
import recipes

@app.route('/status')
def status():
    message = {
        'status':'idle',
        'recipe':None
    }
    return jsonify(message)

@app.route('/list')
def list():
    recipes.refresh()
    return jsonify(recipes.list)

@app.route('/start/<name>')
def start(name):
    (state,msg) = recipes.start(name)
    if state:
        return jsonify({'response':'ok'})
    else:
        return jsonify({'response':'error','message':msg})
