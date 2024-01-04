"""
Starts the two microlab processes, one for the hardware, and the other the
flask backend API.
Starts the flask application on the configured port (default 8081)
Look in api.routes for the actual api code
"""

from multiprocessing import Process, Queue
from microlab import startMicrolabProcess
from api import runFlask
import config


if __name__ == "__main__":
    config.initialSetup()

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
    