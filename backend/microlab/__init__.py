from multiprocessing import Process

class MicrolabInterface:

  def __init__(self, in_queue, out_queue):
    self.q1 = out_queue
    self.q2 = in_queue

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
      self.q1.put({"command": "start", "args": name})

      return self.q2.get()

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
      self.q1.put({"command": "status", "args": None})
      print("sent")
      res = self.q2.get()
      print("waiting")
      return res

  def stop(self):
      """
      Stop the currently running recipe.

      :return:
      None ... at least for now.
      """
      self.q1.put({"command": "stop", "args": None})

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
      self.q1.put({"command": "selectOption", "args": option})
      res = self.q2.get()
      return res
