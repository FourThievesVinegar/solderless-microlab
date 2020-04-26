from api import app
from flask import jsonify
import recipes

@app.route('/list')
def list():
    recipes.refresh()
    return jsonify(recipes.list)

@app.route('/status')
def status():
    return jsonify(recipes.status())

@app.route('/start/<name>')
def start(name):
    (state,msg) = recipes.start(name)
    if state:
        return jsonify({'response':'ok'})
    else:
        return jsonify({'response':'error','message':msg})

@app.route('/stop')
def stop():
    recipes.stop()
    return jsonify({'response':'ok'})

@app.route('/select/option/<name>')
def selectOption(name):
    (state,msg) = recipes.selectOption(name)
    if state:
        return jsonify({'response':'ok'})
    else:
        return jsonify({'response':'error','message':msg})
