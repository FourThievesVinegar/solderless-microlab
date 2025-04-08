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
from recipes.model import MicrolabRecipe, MicrolabRecipeTask
from hardware.core import MicroLabHardware
from datetime import datetime, timedelta, timezone
from enum import Enum
from util.logger import MultiprocessingLogger

from localization import load_translation


class RecipeState(str, Enum):
    IDLE = "idle"
    ERROR = "error"
    RECIPE_UNSUPPORTED = "recipe_unsupported"
    RUNNING = 'running'
    USER_INPUT = 'user_input'
    COMPLETE = 'complete'

class RunningRecipe:
    
    def __init__(self, recipe: MicrolabRecipe, microlabHardware: MicroLabHardware):
        """
        Constructor. Saves the recipe.
        :param recipe:
        The recipe. See module documentation for object description.
        """
        self._logger = MultiprocessingLogger.get_logger(__name__)

        self.step = 0
        self.message = ''
        self.status = RecipeState.IDLE
        self.options = []
        self.icon = ''
        self.stepCompletionTime = None
        self.title = ""
        self.currentTasks = []
        self.recipe = recipe
        if recipe.title:
            self.title = recipe.title

        self._microlabHardware = microlabHardware

    def start(self):
        """
        Start running the recipe. Start from the first step.
        :return:
        None
        """
        t=load_translation()
        
        supported, msg = self.isRecipeSupported(self.recipe)
        if supported:
            self._logger.info(t['starting-recipe'].format(self.title))
            self.step = 0
            self.runStep()
        else:
            self._logger.info(t['recipe-unsupported'].format(self.title, msg))
            self.status = RecipeState.RECIPE_UNSUPPORTED
            self.message = msg

    def isRecipeSupported(self, recipe: MicrolabRecipe):
        t=load_translation()
      
        max = self._microlabHardware.getMaxTemperature()
        minTemp = self._microlabHardware.getMinTemperature()
        for step in recipe.steps:
            for task in step.tasks:
                if "temp" in task.parameters:
                    temp = task.parameters["temp"]
                    if temp > max:
                        return False, t['requires-more-temp'].format(temp, max)
                    if temp < minTemp:
                        return False, t['requires-less-temp'].format(temp, minTemp)
        return True, ''

    def stop(self):
        """
        Stop running the recipe.

        :return:
        None
        """
        t=load_translation()
        
        self._logger.info(t['stopping-recipe'].format(self.title))
        self.step = -1
        if self.status != RecipeState.ERROR:
            self.status = RecipeState.IDLE
            self.message = ''
        self.options = []
        self.stepCompletionTime = None
        self.stopTasks()
        self._microlabHardware.turnOffEverything()

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
                currentStep = self.recipe.getStep(self.step)
                if currentStep.done:
                    self.stop()
                elif currentStep.next:
                    self.step = currentStep.next
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
        t=load_translation()
        
        found = False
        stepOptions = self.recipe.getStep(self.step).options
        if stepOptions:
            for option in stepOptions:
                if option.text == optionValue:
                    self.step = option.next
                    found = True

        if not found:
            return False, t['invalid-option'].format(optionValue)

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
        t=load_translation()
        
        self._logger.info(t['running-step'].format(self.step))
        step = self.recipe.getStep(self.step)
        self._logger.info(t['running-step'].format(step))
        self.message = step.message
        self.stepCompletionTime = None
        self.currentTasks = []
        options: list[str] = []
        tasksToRun = []

        if step.options:
            for option in step.options:
                options.append(option.text)
            if len(options) > 0:
                self.status = RecipeState.USER_INPUT

        self.options = options

        if (step.icon):
            self.icon = step.icon

        if step.baseTask and step.baseTask != 'humanTask': # There are tasks to perform
            # Add the base task
            tasksToRun = [MicrolabRecipeTask(baseTask=step.baseTask,parameters=step.parameters)]
        if step.tasks: # We have other tasks, let's append the base task and those other tasks
            tasksToRun = tasksToRun + step.tasks

        if tasksToRun: # Run all tasks for the step
            for task in tasksToRun:
                if task.baseTask and task.baseTask != 'humanTask':
                    self.currentTasks.append(tasks.runTask(self._microlabHardware, task.baseTask, task.parameters))
            
            tasksWithDurations = filter(
                lambda task: task.parameters and ('time' in task.parameters), tasksToRun)
            taskDurations = list(map(lambda task: task.parameters['time'], tasksWithDurations))
            if len(taskDurations) > 0:
                duration = timedelta(seconds=max(taskDurations))
                self.stepCompletionTime = (datetime.now(tz=timezone.utc) + duration).isoformat()
                
            self.status = RecipeState.RUNNING

        if step.done == True:
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
        t=load_translation()
        
        for task in self.currentTasks:
            if not task["done"] and datetime.now() > task["nextTime"]:
                self._logger.debug("task is ready for next iteration")
                try:
                    res = next(task["fn"])
                    if res == None:
                        self._logger.debug("task is done")
                        task["done"] = True
                    else:
                        duration = timedelta(seconds=res)
                        self._logger.debug(t['task-scheduled'].format(datetime.now() + duration))
                        task["nextTime"] = datetime.now() + duration
                except Exception as e:
                    self._logger.exception(str(e))
                    task["exception"] = e
                    self.status = RecipeState.ERROR
                    self.message = t['task-failed']
                    self.stop()
