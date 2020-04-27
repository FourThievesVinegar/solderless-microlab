import config
from recipes import state

from celery import Celery
from celery.utils.log import get_task_logger

import sys
import os

# Celery changes the current directory after startup so we need to add it to the path.
# Not sure why this would work, I guess it changes it after it initializes the module.
# Either way it works. Reference: https://stackoverflow.com/questions/39438504/dynamically-importing-a-module-in-a-celery-task
sys.path.append(os.getcwd())

logger = get_task_logger(__name__)
if config.celeryMode == 'real':
    app = Celery('recipes',
                  backend=config.celeryBackend,
                  broker=config.celeryBroker)
elif config.celeryMode == 'test':
    from tests import celeryMock
    app = celeryMock

result = None

@app.task
def runInBackground(package,currentRecipe,task,parameters):
    exec('from ' + package + ' import ' + currentRecipe)
    return eval(currentRecipe + '.' + task + '(parameters)')

def runTask(task,parameters):
    global result
    if isTaskComplete():
        result = runInBackground.delay(state.package, state.currentRecipe, task, parameters)
        return True

    return False


def isTaskComplete():
    if not(result is None):
        res = app.AsyncResult(result.task_id)
        return res.ready()

    return True


