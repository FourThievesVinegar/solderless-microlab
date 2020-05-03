from os import listdir
from os.path import isfile, join
from recipes import state

# TODO: This only works if you run the app from the expected directory

def getList():
    path = './' + state.package.replace('.', '/')
    files = [f for f in listdir(path) if isfile(join(path, f))]
    list = []

    for f in files:
        if not f.startswith('__init__'):
            if f.endswith('.py'):
                list.append(f[:-3])

    return list


list = getList()


def refresh():
    global list
    list = getList()


def start(name):
    global list
    if not (state.currentRecipe is None):
        exec('from ' + state.package + '.' + state.currentRecipe + ' import recipe')
        recipeMessage = eval('recipe.getStatus()')
        if not recipeMessage['status'] == 'complete':
            return False,'Recipe ' + state.currentRecipe + ' is running. Stop it first.'
    if not (name in list):
        return False,'Recipe unknown.'

    state.currentRecipe = name
    exec('from ' + state.package + '.' + state.currentRecipe + ' import recipe')
    currentStep = eval('recipe.start()')

    return True,''


# Return the current status of the recipe
def status():
    message = {
        'status':'idle',
        'recipe':state.currentRecipe,
        'step':-1,
        'message':None,
        'options':[]
    }

    if state.currentRecipe == None:
        return message

    exec('from ' + state.package + '.' + state.currentRecipe + ' import recipe')
    recipeMessage = eval('recipe.updateStatus()')
    message['status'] = recipeMessage['status']
    message['step'] = recipeMessage['step']
    message['message'] = recipeMessage['message']
    message['options'] = recipeMessage['options']

    return message


def stop():
    if not state.currentRecipe is None:
        exec('from ' + state.package + '.' + state.currentRecipe + ' import recipe')
        exec('recipe.stop()')
        state.currentRecipe = None


def selectOption(option):
    if not state.currentRecipe is None:
        exec('from ' + state.package + '.' + state.currentRecipe + ' import recipe')
        return eval('recipe.selectOption(option)')
    return False,'No recipe running.'
