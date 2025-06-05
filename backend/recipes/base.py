"""
Common code for recipes, handles running recipe files.

The recipe steps are defined in a json file and they can be strung together with "goto" statements.
Each recipe step can also call a function that changes the desired state of the hardware. These methods are defined
in the tasks.py file and the parameters they accept can be seen in the "baseTask" definition in the
documentation of the plan object below.

You'll probably want to take a look at sample .json recipe in the data/recipes/ directory. This will
give a good idea of what the plan object looks like. For reference, we will also document the plan object here.

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
                is_final
                    When True - signals that this is recipe's final step
"""
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Optional

from hardware.core import MicroLabHardware
from localization import load_translation
from recipes import tasks
from recipes.model import MicrolabRecipe, MicrolabRecipeTask, RecipeTaskRunnable, MicrolabRecipeStep
from util.logger import MultiprocessingLogger


class RecipeState(str, Enum):
    IDLE = 'idle'
    ERROR = 'error'
    RECIPE_UNSUPPORTED = 'recipe_unsupported'
    RUNNING = 'running'
    USER_INPUT = 'user_input'
    COMPLETE = 'complete'


class RunningRecipe:
    def __init__(self, recipe: MicrolabRecipe, microlab_hardware: MicroLabHardware):
        """
        Executes the recipe.
        :param recipe: The recipe. See module documentation for object description.
        """
        self.logger = MultiprocessingLogger.get_logger(__name__)
        self.t = load_translation()

        self.step: int = 0
        self.message: str = ''
        self.status = RecipeState.IDLE
        self.option_names: list[str] = []
        self.icon: str = ''
        self.step_eta: Optional[str] = None
        self.current_tasks: list[RecipeTaskRunnable] = []
        self.recipe: MicrolabRecipe = recipe
        self.title: str = recipe.title if recipe.title else ''

        self.microlab_hardware: MicroLabHardware = microlab_hardware

    def start(self) -> None:
        """
        Start running the recipe. Start from the first step.
        :return:
            None
        """
        supported, msg = self.is_recipe_supported(self.recipe)
        if supported:
            self.logger.info(self.t['starting-recipe'].format(self.title))
            self.step = 0
            self.run_step()
        else:
            self.logger.info(self.t['recipe-unsupported'].format(self.title, msg))
            self.status = RecipeState.RECIPE_UNSUPPORTED
            self.message = msg

    def is_recipe_supported(self, recipe: MicrolabRecipe) -> tuple[bool, str]:
        max_temp = self.microlab_hardware.getMaxTemperature()
        min_temp = self.microlab_hardware.getMinTemperature()
        for step in recipe.steps:
            for task in step.tasks:
                if 'temp' in task.parameters:
                    temp = task.parameters['temp']
                    if temp > max_temp:
                        return False, self.t['requires-more-temp'].format(temp, max_temp)
                    if temp < min_temp:
                        return False, self.t['requires-less-temp'].format(temp, min_temp)
        return True, ''

    def stop(self) -> None:
        """
        Stop running the recipe.

        :return:
        None
        """
        self.logger.info(self.t['stopping-recipe'].format(self.title))
        self.step = -1
        if self.status != RecipeState.ERROR:
            self.status = RecipeState.IDLE
            self.message = ''
        self.option_names = []
        self.step_eta = None
        self.clear_tasks()
        self.microlab_hardware.turnOffEverything()

    def get_status(self) -> dict[str, Any]:
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
            'options': self.option_names,
            'icon': self.icon,
            'stepCompletionTime': self.step_eta,
        }
        return ret

    def check_step_completion(self) -> None:
        """
        Checks if the current step has finished executing, 
        and go to the next if so. If final step is completed, stops
        running the recipes.
        :return:
            None
        """
        if self.status == RecipeState.RUNNING:
            if self.are_tasks_complete():
                current_step = self.recipe.get_step(self.step)
                if current_step.is_final:
                    self.stop()
                elif current_step.next:
                    self.step = current_step.next
                    self.run_step()

    def select_option(self, option_value: str) -> tuple[bool, str]:
        """
        Provide user selected input for the current recipe step.

        :param option_value:
        The name of the selected option. This must be one of the strings presented in the
        "options" list in the get_status() call.

        :return:
        tuple
            boolean
                Whether or not the selection succeeded.
            string
                The message to display to the user in case of failure.
        """
        is_option_found = False
        step_options = self.recipe.get_step(self.step).options
        if step_options:
            for option in step_options:
                if option.text == option_value:
                    self.step = option.next
                    is_option_found = True

        if not is_option_found:
            return False, self.t['invalid-option'].format(option_value)
        else:
            self.run_step()
            return True, self.message

    def run_step(self) -> None:
        """
        Run the current step of the recipe. The actual step advancement management is left
        to the other methods. If you call this method twice for the same step, that step
        will be executed twice.

        :return:
            None
        """
        self.logger.info(self.t['running-step'].format(self.step))
        step: MicrolabRecipeStep = self.recipe.get_step(self.step)
        self.logger.info(self.t['running-step'].format(step))
        self.message = step.message
        self.step_eta = None
        self.current_tasks = []
        option_names: list[str] = []
        tasks_to_run: list[MicrolabRecipeTask] = []

        if step.options:
            for option in step.options:
                option_names.append(option.text)
            if len(option_names) > 0:
                self.status = RecipeState.USER_INPUT
        self.option_names = option_names

        if step.icon:
            self.icon = step.icon

        if step.baseTask and step.baseTask != 'humanTask':
            # Add the base task
            tasks_to_run = [MicrolabRecipeTask(baseTask=step.baseTask, parameters=step.parameters)]
        if step.tasks:
            # This step has additional tasks: append them
            tasks_to_run += step.tasks

        if tasks_to_run:  # Run all tasks for the step
            # Launch all non‐human tasks and collect their generator objects
            self.current_tasks += [
                tasks.run_task(self.microlab_hardware, t.baseTask, t.parameters)
                for t in tasks_to_run if t.baseTask and t.baseTask != 'humanTask'
            ]

            # Compute the maximum 'time' parameter (if any) to set step_eta
            task_durations: list[int] = [t.parameters['time'] for t in tasks_to_run if 'time' in t.parameters]
            if task_durations:
                self.step_eta = (
                    datetime.now(tz=timezone.utc) + timedelta(seconds=max(task_durations))
                ).isoformat()

            self.status = RecipeState.RUNNING

        if step.is_final is True:
            self.status = RecipeState.COMPLETE

    def are_tasks_complete(self) -> bool:
        """
        Check if all currently running tasks have completed.
        :return:
        True
            All tasks are complete.
        False
            Some tasks are still running.
        """
        return all(task.is_done for task in self.current_tasks)

    def clear_tasks(self) -> None:
        """
        clears currently running list of tasks.
        :return:
            None
        """
        self.current_tasks = []

    def tick_tasks(self) -> None:
        """
        Executes one iteration of the current tasks that are scheduled to run.
        :return:
            None
        """
        for task in self.current_tasks:
            if not task.is_done and datetime.now() > task.next_time:
                self.logger.debug('task is ready for next iteration')
                try:
                    res = next(task.fn)
                    if res is None:
                        self.logger.debug('task is done')
                        task.is_done = True
                    else:
                        duration = timedelta(seconds=res)
                        self.logger.debug(self.t['task-scheduled'].format(datetime.now() + duration))
                        task.next_time = datetime.now() + duration
                except Exception as e:
                    self.logger.exception(str(e))
                    task.exception = str(e)
                    self.status = RecipeState.ERROR
                    self.message = self.t['task-failed']
                    self.stop()
                    self.logger.error(f'Stopping recipe {self.recipe.fileName}')
