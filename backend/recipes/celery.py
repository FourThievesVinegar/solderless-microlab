"""
This module gives recipes a simple interface for running methods in the background through celery.

It has 2 modes of operation which are configured in config.celeryMode.
    real
        Makes calls to celery to execute the various tasks in the background and checks for task completion.
    test
        Runs everything in the same thread as it was called in. This is only useful for the unit tests

The only method that needs to be used by the base recipe is runTask(task,parameters). It is documented below.

"""

import requests
import config
from recipes import state, tasks

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

@app.task
def runInBackground(task, parameters):
    """
    Celery task for running a recipe task in the background.

    :param task:
        Task to actually run. This is really just a method to run.

    :param parameters:
        Parameters to pass to the task/method.

    :return:
        Returns any object returned by the recipe task. This is generally None.
    """
    return tasks.tasks[task](parameters)


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

def runTask(task, parameters):
    """
    Run a recipe task/function in the background through Celery.
    These are defined in the tasks.py file.

    :param task:
        Task to run under the currently running recipe.

    :param parameters:
        Parameters to pass to the task. The actual object definition depends on the task.

    :return:
        A celery.result.AsyncResult for the task being executed
    """
    return runInBackground.apply_async((task, parameters), link=updateStatus.s())
