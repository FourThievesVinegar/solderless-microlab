# Start the application on the configured port (default 8081)
# Look in api.routes for the actual api code
import sys
import os 
import config
from microlab.interface import MicrolabInterface
from multiprocessing import Process, Queue
import time
import threading


def runFlask(in_queue, out_queue):
    import api.routes
    from api import app
    reload = False if len(sys.argv) > 1 and sys.argv[1] == 'production' else True

    api.routes.microlabInterface = MicrolabInterface(in_queue, out_queue)
    app.run(host='0.0.0.0', port=config.apiPort)


def startMicrolabProcess(in_queue, out_queue):
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


if __name__ == "__main__":
    q1 = Queue()
    q2 = Queue()

    microlabProcess = Process(target=startMicrolabProcess, args=(q1, q2), name="microlab")
    microlabProcess.start()
    flaskProcess = Process(target=runFlask, args=(q2, q1), name="flask")
    flaskProcess.start()

    microlabProcess.join()
    flaskProcess.join()
    q1.close()
    q2.close()
    q1.join_thread()
    q2.join_thread()
    