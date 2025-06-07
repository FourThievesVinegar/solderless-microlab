"""
Contains function for starting up the microlab process
"""
import queue
import signal
import sys
import threading
from multiprocessing import Queue
from types import FrameType
from typing import Optional, Callable

import hardware.devicelist
import recipes.core
import recipes.state
from config import microlab_config as config
from hardware.core import MicroLabHardware
from localization import load_translation
from util.logger import MultiprocessingLogger

HALT = threading.Event()
MUTEX = threading.Lock()

# Sentinel to signal worker shutdown
SHUTDOWN_SIGNAL = None


def _shutdown_signal_handler(signum: int, frame: Optional[FrameType]) -> None:
    sys.stderr.write('Marking HALT event as SHUTDOWN\n')
    HALT.set()


def run_microlab_thread():
    logger = MultiprocessingLogger.get_logger(__name__)
    try:
        # Loop until HALT is set. Event.wait() returns True if the event was set, else False.
        while not HALT.wait(timeout=0.01):
            with MUTEX:
                if recipes.state.current_recipe:
                    recipes.state.current_recipe.tick_tasks()
                    recipes.state.current_recipe.check_step_completion()
    except Exception:
        logger.exception('Microlab thread crashed')
        HALT.set()
    else:
        logger.info('Microlab thread finished normally')

def reload_hardware() -> tuple[bool, str]:
    microlab_hardware = MicroLabHardware.get_microlab_hardware_controller()
    logger = MultiprocessingLogger.get_logger(__name__)

    t = load_translation()
    logger.info(t['reload-device-config'])
    hardware_config = hardware.devicelist.loadHardwareConfiguration()
    device_definitions = hardware_config['devices']
    return microlab_hardware.loadHardware(device_definitions)


MICROLAB_COMMANDS: dict[str, Callable] = {
    'start': recipes.core.start,
    'status': recipes.core.status,
    'stop': recipes.core.stop,
    'selectOption': recipes.core.select_option,
    'reloadConfig': config.reload_config,
    'reloadHardware': reload_hardware,
}


def start_microlab_process(cmd_queue: Queue, resp_queue: Queue, logging_queue: Queue) -> None:
    """
    Starts up the microlab process

    :param cmd_queue:
        The queue the microlab will listen for commands on

    :param resp_queue:
        The queue responses will be sent to, when applicable.

    :param logging_queue:
        The queue logging messages will be sent through.

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
    # The initialize_logger call only needs to happen once when a new process is started.
    MultiprocessingLogger.initialize_logger(logging_queue)
    logger = MultiprocessingLogger.get_logger(__name__)
    t = load_translation()

    # instantiate MicroLabHardware and start recipes thread
    microlab_hardware = MicroLabHardware.get_microlab_hardware_controller()
    microlab = threading.Thread(target=run_microlab_thread)
    microlab.start()

    signal.signal(signal.SIGINT, _shutdown_signal_handler)
    signal.signal(signal.SIGTERM, _shutdown_signal_handler)

    while True:
        try:
            data = cmd_queue.get(timeout=0.1)  # blocks up to 100 ms
            if data is SHUTDOWN_SIGNAL:
                break
        except queue.Empty:
            if HALT.is_set():
                break
            continue

        command_name = data['command']
        command: Callable = MICROLAB_COMMANDS[command_name]
        if command_name == 'status':
            result = command(data['args'])
        else:
            with MUTEX:
                result = command(data['args'])

        if result is not None:
            resp_queue.put(result)

    logger.info('')
    logger.info(t['shutting-microlab'])
    microlab.join()
    microlab_hardware.turnOffEverything()
    logger.info(t['shutted-microlab'])
