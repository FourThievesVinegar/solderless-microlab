## TODO: This only works if you run the app from the expected directory

from os import listdir
from os.path import isfile, join

def getList():
    path = './recipes'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    list = []

    for f in files:
        if not f.startswith('__init__'):
            if f.endswith('.py'):
                list.append(f[:-3])

    return list

list = getList()
currentRecipe = None

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
    exec('from recipes import ' + name)
    currentStep = eval(name + '.getNextStep()')

    print (currentStep)
    return True,''

# Return the current status of the recipe
def status():
    a = 1

