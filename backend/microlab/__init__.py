"""
Module init.
Contains function for starting up the microlab process
"""

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
    
    import sys
    import time
    import threading
    import hardware
    hardware.microlabHardware = hardware.MicroLabHardware()
    microlabHardware = hardware.microlabHardware
    import recipes
    import signal
    halt = threading.Event()

    def runMicrolab():
        while True:
            time.sleep(0.01)
            if recipes.state.currentRecipe:
                recipes.state.currentRecipe.tickTasks()
            if halt.is_set():
                microlabHardware.turnOffEverything()
                break

    microlab = threading.Thread(target=runMicrolab)
    microlab.start()


    def handleSignal(_a, _b):
        print("")
        print("Shutting down microlab.")
        halt.set()
        microlab.join()
        print("Shutdown completed.")
        sys.exit()

    signal.signal(signal.SIGINT, handleSignal)
    signal.signal(signal.SIGTERM, handleSignal)

    commandDict = {
      "start": recipes.start,
      "status": recipes.status,
      "stop": recipes.stop,
      "selectOption": recipes.selectOption,
    }

    while True:
        time.sleep(0.01)
        if not in_queue.empty():
            data = in_queue.get() # Receive data
            print("received {0}. Queue sizes: {1}, {2}".format(data, in_queue.qsize(), out_queue.qsize()) )
            result = commandDict[data["command"]](data["args"])
            out_queue.put(result) # Send data
