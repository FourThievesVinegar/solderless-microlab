## TODO: This only works if you run the app from the expected directory

from os import listdir
from os.path import isfile, join
import config

package = config.recipesPackage

def getList():
    path = './' + package.replace('.', '/')
    files = [f for f in listdir(path) if isfile(join(path, f))]
    list = []

    for f in files:
        if not f.startswith('__init__'):
            if f.endswith('.py'):
                list.append(f[:-3])

    return list

list = getList()
currentRecipe = None
completedRecipe = None

def refresh():
    global list
    list = getList()

def start(name):
    global list,currentRecipe
    if not currentRecipe is None:
        return False,'Recipe ' + currentRecipe + ' is running. Stop it first.'
    if not (name in list):
        return False,'Recipe unknown.'

    currentRecipe = name
    exec('from ' + package + ' import ' + name)
    currentStep = eval(name + '.start()')

    return True,''

# Return the current status of the recipe
def status():
    global currentRecipe
    message = {
        'status':'idle',
        'recipe':currentRecipe,
        'step':-1,
        'message':None,
        'options':[]
    }
    if currentRecipe is None:
        if not completedRecipe is None:
            message['status'] = 'completed'
            message['recipe'] = completedRecipe
    else:
        exec('from ' + package + ' import ' + currentRecipe)
        message['status'] =  eval(currentRecipe + '.status')
        message['step'] =  eval(currentRecipe + '.step')
        message['message'] =  eval(currentRecipe + '.message')
        message['options'] =  eval(currentRecipe + '.options')
    return message

def stop():
    global currentRecipe
    if not currentRecipe is None:
        exec('from ' + package + ' import ' + currentRecipe)
        exec(currentRecipe + '.stop()')
        currentRecipe = None

def selectOption(option):
    global currentRecipe
    if not currentRecipe is None:
        exec('from ' + package + ' import ' + currentRecipe)
        return eval(currentRecipe + '.selectOption("' + option + '")')
    return False,'No recipe running.'

