"""
This module gives recipes a simple interface for running methods in the background through celery.

It has 2 modes of operation which are configured in config.celeryMode.
    real
        Makes calls to celery to execute the various tasks in the background and checks for task completion.
    test
        Runs everything in the same thread as it was called in. This is only useful for the unit tests

The only method that needs to be used by the base recipe is runTask(task,parameters). It is documented below.

The module is quite simplistic and assumes that only one task is running at any given time.
The link to the task is kept in a global variable called result.

"""

import requests
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

# Check for the running mode
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
    """
    Celery task for running a recipe task in the background.

    :param package:
        Base package for the recipe modules.

    :param currentRecipe:
        Recipe module under which to run the task.

    :param task:
        Task to actually run. This is really just a method to run.

    :param parameters:
        Parameters to pass to the task/method.

    :return:
        Returns any object returned by the recipe task. This is generally None.
    """
    exec('from ' + package + ' import ' + currentRecipe)
    return eval(currentRecipe + '.' + task + '(parameters)')


@app.task
def updateStatus(*args):
    """
    Celery task to notify the web server that a celery task has been completed. Without this method,
    the web server would not know when it can start executing the next step of the recipe.

    :param args:
    :return:
        None
    """
    requests.get(url=config.localUrl + '/status')


def runBaseTask(task,parameters):
    """
    Run a base task/function in the background through Celery.
    These would be define in the recipes.base module

    :param task:
        Task to run under the currently running recipe.

    :param parameters:
        Parameters to pass to the task. The actual object definition depends on the task.

    :return:
        True
            If the celery task was started successfully.
        False
            If there is an already running Celery task.
    """
    runTask(task,parameters,True)


def runTask(task,parameters,base = False):
    """
    Run a recipe task/function in the background through Celery.
    These would be defined the recipe file itself.

    :param task:
        Task to run under the currently running recipe.

    :param parameters:
        Parameters to pass to the task. The actual object definition depends on the task.

    :param base:
        Is this task part of the base module or in the recipe module.

    :return:
        True
            If the celery task was started successfully.
        False
            If there is an already running Celery task.
    """
    global result
    if isTaskComplete():
        if base:
            package = 'recipes'
            recipe = 'base'
        else:
            package = state.package
            recipe = state.currentRecipe
        result = runInBackground.apply_async((package, recipe, task, parameters),link=updateStatus.s())
        return True

    return False


def isTaskComplete():
    """
    Determine if the currently running task has completed.
    :return:
    True
        Task is complete.
    False
        Task is still running.
    """
    if not(result is None):
        res = app.AsyncResult(result.task_id)
        if res.ready():
            res = None
            return True
        else:
            return False

    return True

def stopTask():
    """
    Stop the currently running task.
    :return:
        None
    """
    if result is not None:
        result.revoke(terminate=True)


