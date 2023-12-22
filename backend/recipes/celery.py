"""
This module gives recipes a simple interface for running methods in the background through celery.

It has 2 modes of operation which are configured in config.celeryMode.
    real
        Makes calls to celery to execute the various tasks in the background and checks for task completion.
    test
        Runs everything in the same thread as it was called in. This is only useful for the unit tests

The only method that needs to be used by the base recipe is runTask(task,parameters). It is documented below.

"""

import config
from recipes import state, tasks

from datetime import datetime



def runTask(microlab, task, parameters):
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
    return {
        "fn": tasks.tasks[task](microlab, parameters),
        "parameters": parameters,
        "done": False,
        "nextTime": datetime.now()
    }
