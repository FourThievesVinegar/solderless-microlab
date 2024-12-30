"""
Starts the two microlab processes, one for the hardware, and the other the
flask backend API.
Starts the flask application on the configured port (default 8081)
Look in api.routes for the actual api code
"""
import signal

import config

from multiprocessing import Process, Queue, set_start_method

from api.core import run_flask
from microlab.core import startMicrolabProcess
from util.logger import MultiprocessingLogger


class BackendManager:

    def __init__(self):
        self._q1 = Queue()
        self._q2 = Queue()

        self._processes = []
        self._queues = []

        # The MultiprocessingLogger.initialize_logger call needs to be out of the global scope
        # as it seems if anything that is done that creates a process safe object (in this case a Queue)
        # it seem to 'lock in' the type of process creation and calls to set_start_method('spawn') will
        # throw an exception

        # Additionally the initialize_logger call without any arguments should only happen in the process that
        # is creating other processes
        MultiprocessingLogger.initialize_logger()
        self._logger = MultiprocessingLogger.get_logger(__name__)

    def _are_processes_alive(self) -> bool:
        return any([process.is_alive() for process in self._processes])

    def _cleanup_queues(self):
        self._logger.debug('Cleaning up queues')

        self._q1.close()
        self._q2.close()

        self._q1.join_thread()
        self._q2.join_thread()

        self._logger.debug('Completed cleanup up queues')

    def _cleanup_processes(self):
        self._logger.debug('Cleaning up processes')

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
                    self._logger.debug(f'Attempting to join proc: {proc.pid}')
                    proc.join(timeout=1)

        self._logger.debug('Completed cleaning up processes')

    def _cleanup_everything(self):
        self._cleanup_processes()
        self._cleanup_queues()

    def _handle_exit_signals(self, signum, frame):
        self._logger.debug('Beginning to handle exit signals in BackendManager')
        self._cleanup_everything()
        self._logger.debug('Completed handling exit signals in BackendManager')

    def _start_microlab(self):
        self._microlab_manager_process = Process(
            target=startMicrolabProcess, args=(self._q1, self._q2, MultiprocessingLogger.get_logging_queue()), name="microlab"
        )

        self._processes.append(self._microlab_manager_process)

        self._logger.debug('Starting the microlab process')
        self._microlab_manager_process.start()
        self._logger.debug(f'microlab process pid: {self._microlab_manager_process.pid}')

    def _start_server(self):
        self._flaskProcess = Process(target=run_flask, args=(self._q2, self._q1, MultiprocessingLogger.get_logging_queue()), name="flask", daemon=True)
        self._processes.append(self._flaskProcess)
        self._logger.debug('Starting the server process')
        self._flaskProcess.start()
        print(f'server process pid: {self._flaskProcess.pid}')

    def run(self):
        config.initialSetup()

        self._logger.info("### STARTING MAIN MICROLAB SERVICE ###")

        self._start_microlab()
        self._start_server()

        signal.signal(signal.SIGINT, self._handle_exit_signals)
        signal.signal(signal.SIGTERM, self._handle_exit_signals)

        while self._are_processes_alive() or MultiprocessingLogger.remaining_logs_to_process():
            MultiprocessingLogger.process_logs()

        self._logger.debug("### ENDING MICROLAB SERVICE EXECUTION ###")


def main():
    backend_manager = BackendManager()
    backend_manager.run()


if __name__ == "__main__":
    set_start_method('spawn')
    main()
