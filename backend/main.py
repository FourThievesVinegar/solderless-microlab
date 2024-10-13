"""
Starts the two microlab processes, one for the hardware, and the other the
flask backend API.
Starts the flask application on the configured port (default 8081)
Look in api.routes for the actual api code
"""

import signal

import requests

from multiprocessing import Process, Queue, Value
from microlab.core import MicrolabHardwareManager
from api.core import runFlask
import config
import multiprocessing_logging

import logging
import logging.handlers as handlers
from util.logFormatter import MultiLineFormatter
import sys

from hardware.core import MicroLabHardware


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
        # self._microlab_manager_should_run = Value('i', 1)
        self._q1 = Queue()
        self._q2 = Queue()

    def _shutdown_flask(self):
        shutdown_url = f'http://localhost:{config.microlabConfig.apiPort}/shutdown'
        print(f'_shutdown_flask: shutdown_url: {shutdown_url}')
        response = requests.put(shutdown_url, timeout=1)
        print(f'_shutdown_flask: response code: {response.status_code}')
        # try:
        # self._flaskProcess.terminate()
        # except ValueError as e:
        #     print(e)
        #     # When you terminate the process this way it will kill it however it will
        #     # raise a secondary exception when killing the process, claiming there is no process to kill
        #     # even though there certainly is. I suspect this may be Flasks behavior in how it handles signals
        #     pass

        # except AttributeError as e:
        #     print(e)
        #     pass

    def _handle_exit_signals(self, signum, frame):
        print('in _handle_exit_signals')
        # self._shutdown_flask()
        print('cleaing q1')
        while not self._q1.empty():
            self._q1.get()
        print('cleaing q2')
        while not self._q2.empty():
            self._q2.get()
        print('cleaing done')
        # self._microlab_manager_should_run.value = 0
        # print('in _handle_exit_signals closing queue 1')
        # self._q1.close()
        # print('in _handle_exit_signals closing queue 2')
        # self._q2.close()
        # print('in _handle_exit_signals queues closed')
        
    def run(self):
        config.initialSetup()
        setupLogging()

        logging.info("### STARTING MAIN MICROLAB SERVICE ###")

        print('MAIN before')
        # We're setting up a shared memory value here so that if the main process recieves a signal to terminate
        # we can update the value to indicate to the process that it needs to terminate
        
        self._microlab_hardware = MicroLabHardware.get_microlab_hardware_controller()
        # self._microlab_manager = MicrolabHardwareManager(
        #     self._microlab_hardware, q1, q2, self._microlab_manager_should_run
        # )
        self._microlab_manager_process = MicrolabHardwareManager(
            self._microlab_hardware, self._q1, self._q2
        )
        print('MAIN before lab start')
        # self._microlab_manager_process = Process(target=self._microlab_manager.run, name="microlab")
        self._microlab_manager_process.start()
        print(f'MAIN self._microlab_manager_process pid: {self._microlab_manager_process.pid}')

        self._flaskProcess = Process(target=runFlask, args=(self._q2, self._q1), name="flask", daemon=True)
        print('MAIN before flask start')
        self._flaskProcess.start()

        print(f'MAIN self._flaskProcess pid: {self._flaskProcess.pid}')
        signal.signal(signal.SIGINT, self._handle_exit_signals)
        signal.signal(signal.SIGTERM, self._handle_exit_signals)

        print('MAIN before flask join')
        self._flaskProcess.join()

        print('MAIN before lab join')
        try:
            self._microlab_manager_process.join()
        except Exception as e:
            # We re-raise any exceptions in execution and if we see them we need to shut down flask
            print(f'Hit lab exception: {e}')
            self._shutdown_flask()
            # raise
            import sys
            sys.exit(1)

        print('MAIN before q1 close')
        self._q1.close()
        print('MAIN before q1 join')
        self._q1.join_thread()
        print('MAIN before q2 close')
        self._q2.close()
        print('MAIN before q2 join')
        self._q2.join_thread()
        print('MAIN run done')
        # sys.exit(0)


def main():
    backend_manager = BackendManager()
    backend_manager.run()


if __name__ == "__main__":
    main()
