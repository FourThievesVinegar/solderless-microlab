"""
Contains function for starting up the microlab process
"""
import logging
import time
import traceback
import signal
import os

import hardware.devicelist
import recipes.core
import recipes.state

# from threading import Thread, Event, Lock
from multiprocessing import Queue, Process
from typing import Optional

from config import microlabConfig as config
from hardware.core import MicroLabHardware


# HALT = Event()
# MUTEX = Lock()

LOGGER = logging.getLogger(__name__)


class MicrolabHardwareManager(Process):

    def __init__(
        self, microlab_hardware: MicroLabHardware, in_queue: Queue, out_queue: Queue, should_run: int,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._microlab_hardware: MicroLabHardware = microlab_hardware
        self._in_queue = in_queue
        self._out_queue = out_queue
        # should_run is actually a multiprocessing.Value that is an int, if the main thread recieves a signal
        # to exit it will update this shared value. It is typed as an int as opposed to multiprocessing.Value
        # because when typed as a 'Value' (by mypy at least) it shows as an invalid type
        self._should_run = should_run

        self._command_dict = {
                "start": recipes.core.start,
                "status": recipes.core.status,
                "stop": recipes.core.stop,
                "selectOption": recipes.core.selectOption,
                "reloadConfig": config.reloadConfig,
                "reloadHardware": self._reload_hardware,
            }

        self._execution_exception = None

    def _setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)

    def _shutdown(self, signum, frame):
        LOGGER.info('Begining microlab shutdown process.')
        self._should_run = 0

    def _cleanup(self):
        LOGGER.info("")
        LOGGER.info("Shutting down microlab.")
        self._microlab_hardware.turnOffEverything()
        LOGGER.info("Shutdown completed.")
        os._exit(os.EX_OK)
        # import sys
        # sys.exit()
        # self._out_queue.close()

    def _run_command(self, command_string: str, command_args: Optional[str]) -> Optional[str]:
        result = None
        command = self._command_dict[command_string]

        if command_args:
            result = command(command_args)
        else:
            result = command()

        return result

    def _update_queue_data(self):
        if not self._in_queue.empty():
            data = self._in_queue.get(timeout=5)  # Receive data
            # status just fetches data and so doesn't need a lock, everything
            # else is a mutation and needs a lock to prevent conflicts with
            # the other thread
            result = self._run_command(data["command"], data.get("args", None))
            if result is not None:
                self._out_queue.put(result, timeout=5)  # Send data back

        # while True:
        #     time.sleep(0.01)
        #     if not self._in_queue.empty():
        #         data = self._in_queue.get() # Receive data
        #         # status just fetches data and so doesn't need a lock, everything
        #         # else is a mutation and needs a lock to prevent conflicts with
        #         # the other thread
        #         if data["command"] == "status":
        #             result = self._command_dict[data["command"]](data["args"])
        #         else:
        #             with self._lock:
        #                 if data["args"]:
        #                     result = self._command_dict[data["command"]](data["args"])
        #                 else:
        #                     result = self._command_dict[data["command"]]

        #         if result is not None:
        #             self._out_queue.put(result)  # Send data back

    def _update_microlab(self):
        if recipes.state.currentRecipe:
            recipes.state.currentRecipe.tickTasks()
            recipes.state.currentRecipe.checkStepCompletion()
            
        # if HALT.is_set():
        #     self._microlab_hardware.turnOffEverything()
        #     break

    def _reload_hardware(self):
        LOGGER.info("Reloading microlab device configuration")
        hardwareConfig = hardware.devicelist.loadHardwareConfiguration()
        deviceDefinitions = hardwareConfig['devices']
        return self._microlab_hardware.loadHardware(deviceDefinitions)

    def run(self):
        # We setup signal handlers here as this is what is the target of (multiprocessing) Process.run. 
        # If signal handlers are setup before existing in their own process they will be setup for the
        # base context *and* be inherited by the new Process being started
        self._setup_signal_handlers()

        # Any non-zero value will evalutate to True, self._should_run can be changed by either
        # the spawning process recieving an exit signal and updating the value (it is a multiprocess.Value),
        # or this process recieving an exit signal directly. This way we should make a best effort to shutdown
        # the associated hardware
        while self._should_run:
            # print('run loop pre sleep')
            time.sleep(0.01)
            try:
                # print('run loop pre _update_queue_data')
                self._update_queue_data()
                # print('run loop pre _update_microlab')
                self._update_microlab()
                # print('run loop post _update_microlab')
            except Exception as e:
                self._execution_exception = e
                LOGGER.error(f'While running microlab hardware encountered exception: {e}. Shutting down microlab.')
                LOGGER.debug(traceback.print_exc())
                break

        # print('run loop pre _cleanup')
        self._cleanup()
        # print('run loop post _cleanup')

    # def join(self, *args, **kwargs):
    #     super().join(*args, **kwargs)

    #     if self._execution_exception:
    #         raise self._execution_exception


# def startMicrolabProcess(in_queue, out_queue):
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
    # microlabHardware = MicroLabHardware.get_microlab_hardware_controller()

    # def runMicrolab():
    #     while True:
    #         time.sleep(0.01)
    #         MUTEX.acquire()
    #         if recipes.state.currentRecipe:
    #             recipes.state.currentRecipe.tickTasks()
    #             recipes.state.currentRecipe.checkStepCompletion()
    #         MUTEX.release()
            
    #         if HALT.is_set():
    #             microlabHardware.turnOffEverything()
    #             break

    # microlab = threading.Thread(target=runMicrolab)
    # microlab.start()

    # def handleSignal(_a, _b):
    #     logging.info("")
    #     logging.info("Shutting down microlab.")
    #     HALT.set()
    #     microlab.join()
    #     logging.info("Shutdown completed.")
    #     sys.exit()

    # signal.signal(signal.SIGINT, handleSignal)
    # signal.signal(signal.SIGTERM, handleSignal)

    # def reloadHardware():
    #     logging.info("Reloading microlab device configuration")
    #     hardwareConfig = hardware.devicelist.loadHardwareConfiguration()
    #     deviceDefinitions = hardwareConfig['devices']
    #     return microlabHardware.loadHardware(deviceDefinitions)

    # commandDict = {
    #   "start": recipes.core.start,
    #   "status": recipes.core.status,
    #   "stop": recipes.core.stop,
    #   "selectOption": recipes.core.selectOption,
    #   "reloadConfig": lambda x: config.reloadConfig(),
    #   "reloadHardware": lambda x: reloadHardware(),
    # }

    # while True:
    #     time.sleep(0.01)
    #     if not in_queue.empty():
    #         data = in_queue.get() # Receive data
    #         # status just fetches data and so doesn't need a lock, everything
    #         # else is a mutation and needs a lock to prevent conflicts with
    #         # the other thread
    #         if data["command"] == "status":
    #             result = commandDict[data["command"]](data["args"])
    #         else:
    #             MUTEX.acquire()
    #             result = commandDict[data["command"]](data["args"])
    #             MUTEX.release()
    #         if result is not None:
    #             out_queue.put(result) # Send data back
