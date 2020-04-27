import config
from recipes import package
from recipes import currentRecipe

from celery import Celery
from celery.utils.log import get_task_logger


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
    global result, package, currentRecipe
    if isTaskComplete():
        result = runInBackground.delay(package, currentRecipe, task, parameters)
        return True

    return False


def isTaskComplete():
    if not(result is None):
        res = app.AsyncResult(result.task_id)
        return res.ready()

    return True


