"""
Contains function for starting up the microlab process
"""
import threading

from hardware.core import MicroLabHardware

HALT = threading.Event()
MUTEX = threading.Lock()


def startMicrolabProcess(in_queue, out_queue):
    """
    Starts up the microlab process

    :param in_queue:
        The queue the microlab will listen for commands on

    :param out_queue:
        The queue responses will be sent to, when applicable.

    All commands sent over the queue have the following format:

    dict
        command
            String with the following values: 
                "start"
                "stop"
                "status"
                "selectOption"
        args
            structure is determined by command type, see following section


    Supported command and return values:
        "start":
            Begins the execution of a recipe
            args structure
                string - name of the recipe to start execution
            returns
                (True, '') on success.
                (False, message) on failure.
            reference "start" in /recipes/__init__.py for more info
        "stop":
            Stops the execution of a recipe
            args structure
                None
            returns
                None
            reference "stop" in /recipes/__init__.py for more info
        "status":
            Gets the status of the microlab
            args structure
                None
            returns
                large object, see reference            
            reference "status" in /recipes/__init__.py for more info
        "selectOption":
            Selects an option when a recipe requires user input
            args structure
                string - option the user selected
            returns
                (True, '') on success.
                (False, message) on failure.
            reference "selectOption" in /recipes/__init__.py for more info
    """
    import logging
    import sys
    import time

    import hardware.devicelist
    import recipes.core
    import recipes.state
    import signal
    from config import microlabConfig as config

    microlabHardware = MicroLabHardware.get_microlab_hardware_controller()

    def runMicrolab():
        while True:
            time.sleep(0.01)
            MUTEX.acquire()
            if recipes.state.currentRecipe:
                recipes.state.currentRecipe.tickTasks()
                recipes.state.currentRecipe.checkStepCompletion()
            MUTEX.release()
            
            if HALT.is_set():
                microlabHardware.turnOffEverything()
                break

    microlab = threading.Thread(target=runMicrolab)
    microlab.start()

    def handleSignal(_a, _b):
        logging.info("")
        logging.info("Shutting down microlab.")
        HALT.set()
        microlab.join()
        logging.info("Shutdown completed.")
        sys.exit()

    signal.signal(signal.SIGINT, handleSignal)
    signal.signal(signal.SIGTERM, handleSignal)

    def reloadHardware():
        logging.info("Reloading microlab device configuration")
        hardwareConfig = hardware.devicelist.loadHardwareConfiguration()
        deviceDefinitions = hardwareConfig['devices']
        return microlabHardware.loadHardware(deviceDefinitions)

    commandDict = {
      "start": recipes.core.start,
      "status": recipes.core.status,
      "stop": recipes.core.stop,
      "selectOption": recipes.core.selectOption,
      "reloadConfig": lambda x: config.reloadConfig(),
      "reloadHardware": lambda x: reloadHardware(),
    }

    while True:
        time.sleep(0.01)
        if not in_queue.empty():
            data = in_queue.get() # Receive data
            # status just fetches data and so doesn't need a lock, everything
            # else is a mutation and needs a lock to prevent conflicts with
            # the other thread
            if data["command"] == "status":
                result = commandDict[data["command"]](data["args"])
            else:
                MUTEX.acquire()
                result = commandDict[data["command"]](data["args"])
                MUTEX.release()
            if result is not None:
                out_queue.put(result) # Send data back
