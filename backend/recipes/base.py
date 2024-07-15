"""
Common code for recipes, handles running recipe files.

The recipe steps are defined in a json file and they can be strung together with "goto" statements.
Each recipe step can also call a function that changes the desired state of the hardware. These methods are defined
in the tasks.py file and the parameters they accept can be seen in the "baseTask" definition in the
documentation of the plan object below.

You'll probably want to take a look at sample recipe in the recipes.files package. This will
give a good idea of what the plan object looks like. For reference we will also document the
plan object here.

plan object
    title
        Name of the recipe that is displayed to the user
        Needs to be a unique string
    materials
        List of materials needed for the recipe
        array of:
            object
                description
                    Description of the material
    steps
        array of:
            object
                nr
                    Step number. Should be an unique integer.
                    You'll use this id in the plan to string steps together.
                message
                    The message to display to the user for this step.
                    Even if the step doesn't have any user input it should
                    tell the user what the application is doing.
                next
                    The nr id of the next step to execute.
                    This is ignored if the step has options.
                icon
                    Optional.
                    String indicating which icon to display on the frontend.
                    If unspecified defaults to the last displayed icon, or a
                    spinning logo if an icon was never specified.
                    One of:
                        reaction_chamber
                        load_syringe
                        inspect
                        dispensing
                        temperature
                        reaction_complete
                options
                    array of:
                        object
                            text
                                Text to display to the user as an option
                            next
                                The nr id of the step to execute if the
                                user picks this option.
                tasks
                    array of:
                    object
                        baseTask
                            Name of the function to execute in the recipes.tasks module.
                            One of:
                                heat
                                    parameters: {'temp': 65}
                                cool
                                    parameters: {'temp': 5}
                                maintainCool
                                    parameters: {'time': 600, 'temp': 5, 'tolerance': 2}
                                maintainHeat
                                    parameters: {'time': 600, 'temp': 65, 'tolerance': 2}
                                maintain
                                    parameters: {'time': 600, 'temp': 65, 'tolerance': 2, 'type': 'heat'}
                                pump
                                    parameters: {'pump':'X','volume': 50}
                                stir
                                    parameters: {'time': 60}
                        parameters
                            The parameters to pass to the task function. This
                            is a dictionary that will be passed as the single
                            parameter to this function.
                done
                    Always set to true and signals that the recipe was
                    successfully completed.
"""

from recipes import tasks
from hardware import microlabHardware
from datetime import datetime, timedelta, timezone
import traceback
from enum import Enum
import logging

class RecipeState(str, Enum):
    IDLE = "idle"
    ERROR = "error"
    RECIPE_UNSUPPORTED = "recipe_unsupported"
    RUNNING = 'running'
    USER_INPUT = 'user_input'
    COMPLETE = 'complete'


RECIPE_STEPS = 'steps'
STEP_TASKS = 'tasks'
TASK_TYPE = 'baseTask'
TASK_PARAMETERS = 'parameters'
NEXT_STEP = 'next'
STEP_USER_OPTIONS = 'options'
LAST_STEP = 'done'

class Recipe:
    
    def __init__(self, plan):
        """
        Constructor. Saves the plan.
        :param plan:
        The recipe plan. See module documentation for object description.
        """
        self.step = 0
        self.message = ''
        self.status = RecipeState.IDLE
        self.options = []
        self.icon = ''
        self.stepCompletionTime = None
        self.currentRecipe = None
        self.currentTasks = []
        self.plan = plan
        if 'title' in plan:
            self.currentRecipe = plan['title']

    def start(self):
        """
        Start running the recipe. Start from the first step.
        :return:
        None
        """
        supported, msg = self.isRecipeSupported(self.plan)
        if supported:
            logging.info('Starting recipe {0}'.format(self.currentRecipe))
            self.step = 0
            self.runStep()
        else:
            logging.info('Recipe {0} unsupported: {1}'.format(self.currentRecipe, msg))
            self.status = RecipeState.RECIPE_UNSUPPORTED
            self.message = msg

    def isRecipeSupported(self, recipe):
        max = microlabHardware.getMaxTemperature()
        minTemp = microlabHardware.getMinTemperature()
        for step in recipe[RECIPE_STEPS]:
            if STEP_TASKS in step:
                for task in step[STEP_TASKS]:
                    if "temp" in task[TASK_PARAMETERS]:
                        temp = task[TASK_PARAMETERS]["temp"]
                        if temp > max:
                            return False, "Recipe requires temperature of {0}C, which is higher than your current hardware supports ({1}C).".format(temp, max)
                        if temp < minTemp:
                            return False, "Recipe requires temperature of {0}C, which is lower than your current hardware supports ({1}C).".format(temp, minTemp)
        return True, ''

    def stop(self):
        """
        Stop running the recipe.

        :return:
        None
        """
        logging.info('Stopping recipe {0}'.format(self.currentRecipe))
        self.step = -1
        if self.status != RecipeState.ERROR:
            self.status = RecipeState.IDLE
            self.message = ''
        self.options = []
        self.stepCompletionTime = None
        self.stopTasks()
        microlabHardware.turnOffEverything()

    def getStatus(self):
        """
        Get the current status of the recipe. This would be updated after
        each step is run.
        :return:
        object
            status
                The state of the recipe. One of:
                    idle
                        App is waiting for the user to start a recipe
                    running
                        App is running a recipe and doesn't need any input from the user
                    user_input
                        App is waiting for the user to make a decision. See options.
                    complete
                        Recipe is complete.
                    error
                        A system error has occurred.
            step
                The current running step
            message
                The message that should be displayed to the user for the currently running step
            options
                null or a list of strings to display to the user as selectable options.
            stepCompletionTime
                An ISO date string for when the current step is expected to be completed, or None
                if unknown. 
        """
        ret = {
            'status': self.status,
            'step': self.step,
            'message': self.message,
            'options': self.options,
            'icon': self.icon,
            'stepCompletionTime': self.stepCompletionTime,
        }
        return ret

    def checkStepCompletion(self):
        """
        Checks if the current step has finished executing, 
        and go to the next if so. If final step is completed, stops
        running the recipes.
        :return:
        None
        """
        if self.status == RecipeState.RUNNING:
            if self.areTasksComplete():
                currentStep = self.plan[RECIPE_STEPS][self.step]
                if(LAST_STEP in currentStep) and (currentStep[LAST_STEP] == True):
                    self.stop()
                else:
                    if NEXT_STEP in currentStep:
                        self.step = currentStep[NEXT_STEP]
                        self.runStep()

    def selectOption(self, optionValue):
        """
        Provide user selected input for the current recipe step.

        :param optionValue:
        The name of the user selected option. This must be one of the strings presented in the
        "options" list in the getStatus() call.

        :return:
        list
            boolean
                Whether or not the selection succeeded.
            string
                The message to display to the user in case of failure.
        """
        found = False
        if STEP_USER_OPTIONS in self.plan[RECIPE_STEPS][self.step]:
            for option in self.plan[RECIPE_STEPS][self.step][STEP_USER_OPTIONS]:
                if option['text'] == optionValue:
                    self.step = option[NEXT_STEP]
                    found = True

        if not found:
            return False, 'Invalid option {0}'.format(optionValue)

        ret = self.runStep()
        return ret, self.message

    def runStep(self):
        """
        Run the current step of the recipe. The actual step advancement management is left
        to the other methods. If you call this method twice for the same step, that step
        will be executed twice.

        :return:
        list
            boolean
                Whether or not the selection succeeded.
            string
                The message to display to the user in case of failure.
        """
        logging.info('Running step {0}'.format(self.step))
        step = self.plan[RECIPE_STEPS][self.step]
        self.message = step['message']
        self.stepCompletionTime = None
        self.currentTasks = []
        options = []
        tasksToRun = []

        if STEP_USER_OPTIONS in step:
            for option in step[STEP_USER_OPTIONS]:
                options.append(option['text'])
            if len(options) > 0:
                self.status = RecipeState.USER_INPUT

        self.options = options

        if('icon' in step):
            self.icon = step['icon']

        if TASK_TYPE in step and step[TASK_TYPE] != 'humanTask': # There are tasks to perform
            # Add the base task
            tasksToRun = [{TASK_TYPE: step[TASK_TYPE], TASK_PARAMETERS: step[TASK_PARAMETERS]}]
            if STEP_TASKS in step: # We have other tasks, let's append the base task and those other tasks
                tasksToRun = tasksToRun + step[STEP_TASKS]

        if tasksToRun: # Run all tasks for the step
            for task in tasksToRun:
                if TASK_TYPE in task and task[TASK_TYPE] != 'humanTask':
                    self.currentTasks.append(tasks.runTask(microlabHardware, task[TASK_TYPE], task[TASK_PARAMETERS]))
            
            tasksWithDurations = filter(
                lambda task: (TASK_PARAMETERS in task) and ('time' in task[TASK_PARAMETERS]), tasksToRun)
            taskDurations = list(map(lambda task: task[TASK_PARAMETERS]['time'], tasksWithDurations))
            if len(taskDurations) > 0:
                duration = timedelta(seconds=max(taskDurations))
                self.stepCompletionTime = (datetime.now(tz=timezone.utc) + duration).isoformat()
                
            self.status = RecipeState.RUNNING

        if step.get(LAST_STEP, False) == True:
            self.status = RecipeState.COMPLETE

        return True

    def areTasksComplete(self):
        """
        Check if all currently running tasks have completed.
        :return:
        True
            All tasks are complete.
        False
            Some tasks are still running.
        """
        return all(task["done"] for task in self.currentTasks)

    def stopTasks(self):
        """
        Stop the currently running tasks.
        :return:
            None
        """
        # for task in self.currentTasks:
        #     task.cancel()
        self.currentTasks = []

    def tickTasks(self):
        """
        Executes one iteration of the current tasks that are scheduled to run.
        :return:
            None
        """
        for task in self.currentTasks:
            if not task["done"] and datetime.now() > task["nextTime"]:
                logging.debug("task is ready for next iteration")
                try:
                    res = next(task["fn"])
                    if res == None:
                        logging.debug("task is done")
                        task["done"] = True
                    else:
                        duration = timedelta(seconds=res)
                        logging.debug("task is scheduled for {0}".format(datetime.now() + duration))
                        task["nextTime"] = datetime.now() + duration
                except Exception as e:
                    logging.exception(str(e))
                    task["exception"] = e
                    self.status = RecipeState.ERROR
                    self.message = 'Task execution failed.'
                    self.stop()


