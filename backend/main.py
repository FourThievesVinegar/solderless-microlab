"""
Starts the two microlab processes, one for the hardware, and the other the
flask backend API.
Starts the flask application on the configured port (default 8081)
Look in api.routes for the actual api code
"""
import sys
import time
import signal
import logging
import logging.handlers as handlers

import multiprocessing_logging

import config

from multiprocessing import Process, Queue, set_start_method

from api.core import run_flask
from microlab.core import startMicrolabProcess
from util.logFormatter import MultiLineFormatter

LOGGER = logging.getLogger(__name__)


def setupLogging():
    logHandlers = []
    formatter = MultiLineFormatter(fmt="%(asctime)s [%(levelname)s]: %(message)s")

    fileLogger = handlers.RotatingFileHandler(
        "{0}/microlab.log".format(config.microlabConfig.logDirectory),
        maxBytes=config.microlabConfig.logFileMaxBytes,
        backupCount=config.microlabConfig.logFileBackupCount,
    )
    fileLogger.setFormatter(formatter)
    logHandlers.append(fileLogger)
    if config.microlabConfig.logToStderr:
        stderrLogger = logging.StreamHandler(sys.stderr)
        stderrLogger.setFormatter(formatter)
        logHandlers.append(stderrLogger)

    logging.basicConfig(handlers=logHandlers, level=config.microlabConfig.logLevel)
    multiprocessing_logging.install_mp_handler()


class BackendManager:

    def __init__(self):
        self._q1 = Queue()
        self._q2 = Queue()

        self._processes = []
        self._queues = []

    def _are_processes_alive(self) -> bool:
        return any([process.is_alive() for process in self._processes])

    def _cleanup_queues(self):
        LOGGER.debug('Cleaning up queues')

        self._q1.close()
        self._q2.close()

        self._q1.join_thread()
        self._q2.join_thread()

        LOGGER.debug('Completed cleanup up queues')

    def _cleanup_processes(self):
        LOGGER.debug('Cleaning up processes')

        while self._are_processes_alive():
            for proc in self._processes:
                try:
                    self._q1.get_nowait()
                except Exception:
                    pass

                try:
                    self._q2.get_nowait()
                except Exception:
                    pass

                if proc.is_alive():
                    LOGGER.debug(f'Attempting to join proc: {proc.pid}')
                    proc.join(timeout=1)

        LOGGER.debug('Completed cleaning up processes')

    def _cleanup_everything(self):
        self._cleanup_processes()
        self._cleanup_queues()

    def _handle_exit_signals(self, signum, frame):
        LOGGER.debug('Beginning to handle exit signals in BackendManager')
        self._cleanup_everything()
        LOGGER.debug('Completed handling exit signals in BackendManager')

    def _start_microlab(self):
        self._microlab_manager_process = Process(
            target=startMicrolabProcess, args=(self._q1, self._q2), name="microlab"
        )

        self._processes.append(self._microlab_manager_process)

        LOGGER.debug('Starting the microlab process')
        self._microlab_manager_process.start()
        LOGGER.debug(f'microlab process pid: {self._microlab_manager_process.pid}')

    def _start_server(self):
        self._flaskProcess = Process(target=run_flask, args=(self._q2, self._q1), name="flask", daemon=True)
        self._processes.append(self._flaskProcess)
        LOGGER.debug('Starting the server process')
        self._flaskProcess.start()
        print(f'server process pid: {self._flaskProcess.pid}')

    def run(self):
        config.initialSetup()

        LOGGER.info("### STARTING MAIN MICROLAB SERVICE ###")

        self._start_microlab()
        self._start_server()

        signal.signal(signal.SIGINT, self._handle_exit_signals)
        signal.signal(signal.SIGTERM, self._handle_exit_signals)

        while self._are_processes_alive():
            time.sleep(0.1)

        LOGGER.debug("### ENDING MICROLAB SERVICE EXECUTION ###")


def main():
    backend_manager = BackendManager()
    backend_manager.run()


if __name__ == "__main__":
    set_start_method('spawn')
    setupLogging()
    main()
