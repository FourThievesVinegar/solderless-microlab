"""
Module init.
Contains function for starting up the microlab process
"""

def startMicrolabProcess(in_queue, out_queue):
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
