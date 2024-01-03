

class MicrolabInterface:
  """
  Interface for the flask process to communicate with the microlab process.

  At the moment the functionality mostly mirrors the functions in 
  /recipe/__init__.py, though this will change.

  For extending this with additional functionality, see /microlab/__init__.py 
  for info on implementing commands.
  """

  def __init__(self, in_queue, out_queue):
    self.toMicrolab = out_queue
    self.fromMicrolab = in_queue

  def start(self, name):
      """
      Start running a recipe.

      A recipe can only be started if the current state of the machine is idle or complete
      and the recipe exists in the list of recipes.
      :param name:
      The name of the recipe. Must be the title of an element of the recipes.list list.
      :return:
      (True, '') on success.
      (False, message) on failure.
      """
      # Validate that the microlab hardware controller has initialized
      self.toMicrolab.put({"command": "start", "args": name})

      return self.fromMicrolab.get()

  def status(self):
      """
      Get the status of the machine.
      :return:
      object
          message
              The message to be displayed to the user.
          options
              null or a list of strings to display to the user as selectable options.
          recipe
              Name of the currently running recipe or null if none is running.
          step
              The step number or -1 if no recipe is running
          status
              The state of the application. One of:
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
          icon
              The icon to show in the UI. See StatusIcon.jsx for supported icons.
          stepCompletionTime
              An ISO date string for when the current step is expected to be completed,
              or null if unknown. 
      """
      self.toMicrolab.put({"command": "status", "args": None})
      res = self.fromMicrolab.get()
      return res

  def stop(self):
      """
      Stop the currently running recipe.

      :return:
      None ... at least for now.
      """
      self.toMicrolab.put({"command": "stop", "args": None})

  def selectOption(self, option):
      """
      Pass in the user selected option from a recipe step.

      The current step must have provided a list of options through the /status API
      and the option must be part of the list provided as an option.
      :param option:
      The selected option. It must be part of the options list as retrieved via /status
      :return:
      (True,'') on success
      (False,message) on failure
      """
      self.toMicrolab.put({"command": "selectOption", "args": option})
      res = self.fromMicrolab.get()
      return res
