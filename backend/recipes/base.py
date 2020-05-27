"""
Common code for recipes. While it is not strictly necessary for a recipe to extend this class,
it does make things a lot easier as it provides recipe step management. If you really don't
want to inherit from this class just create a class with the same name and interface in your
recipe file.

If you do use this class, the recipe steps are defined in a plan object and they can be strung
together with "goto" statements. Each recipe step also has the option to call celery with a
method to execute. The method would be defined in the actual recipe file to allow for arbitrary
hardware functionality.

You'll probably want to take a look at sample recipe in the recipes.files package. This will
give a good idea of what the plan object looks like. For reference we will also document the
plan object here.

plan object
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
                options
                    array of:
                        object
                            text
                                Text to display to the user as an option
                            next
                                The nr id of the step to execute if the
                                user picks this option.
                task
                    Name of the function to execute as a celery task.
                    This function should be implemented in the same package
                    that defines the plan.
                    TODO: Stop requirements once I figure them out.
                parameters
                    The parameters to pass to the task function. This
                    is a dictionary that will be passed as the single
                    parameter to this function.
                done
                    Always set to True and signals that the recipe was
                    successfully completed.
"""

from recipes import celery

class Recipe:
    step = 0
    message = ''
    status = 'idle'
    options = []

    def __init__(self, plan):
        """
        Constructor. Saves the plan.
        :param plan:
        The recipe plan. See module documentation for object description.
        """
        self.plan = plan


    def start(self):
        """
        Start running the recipe. Start from the first step.
        :return:
        None
        """
        self.step = 0
        self.runStep()


    def stop(self):
        """
        Stop running the recipe.

        TODO: figure out how to stop any running celery tasks
        :return:
        None
        """
        self.step = -1
        self.status = 'idle'
        self.message = ''
        self.options = []


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
        """
        ret = {
            'status':self.status,
            'step':self.step,
            'message':self.message,
            'options':self.options
        }
        return ret


    def updateStatus(self):
        """
        Updates the current status and then returns it. This effectively polls the celery task
        to see if it has completed.
        :return:
        object
            Same as getStatus()
        """
        if self.status == 'running':
            if celery.isTaskComplete():
                self.step = self.plan['steps'][self.step]['next']
                self.runStep()

        return self.getStatus()


    def selectOption(self,optionValue):
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
        if 'options' in self.plan['steps'][self.step]:
            for option in self.plan['steps'][self.step]['options']:
                if option['text'] == optionValue:
                    self.step = option['next']
                    found = True

        if not found:
            return False, 'Invalid option ' + optionValue

        ret = self.runStep()
        return ret,self.message


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
        print('Running step ' + str(self.step))
        step = self.plan['steps'][self.step]
        self.message = step['message']
        options = []

        if 'options' in step:
            for option in step['options']:
                options.append(option['text'])
            if len(options) > 0:
                self.status = 'user_input'

        self.options = options

        if 'task' in step:
            if celery.runTask(step['task'], step['parameters']):
                self.status = 'running'
            else:
                self.status = 'error'
                message = 'Internal error. Task already running.'
                return False

        if 'done' in step:
            if step['done'] == True:
                self.status = 'complete'

        return True
