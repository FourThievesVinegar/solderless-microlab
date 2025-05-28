"""
Starts the two microlab processes (hardware & Flask API),
manages clean startup/shutdown, and processes logs.
"""
import signal
from multiprocessing import Process, Queue, set_start_method
from typing import List, Optional
from types import FrameType

import config
from config import microlabConfig
from api.core import start_flask_process
from microlab.core import start_microlab_process
from util.logger import MultiprocessingLogger
from localization import load_translation

# Sentinel to signal worker shutdown
SHUTDOWN_SIGNAL = None


class BackendManager:
    def __init__(self) -> None:
        self.t = load_translation()

        # Prepare logger (initialized in *main*)
        self.logger = MultiprocessingLogger.get_logger(__name__)

        # Command & response queues
        self.cmd_queue: Queue = Queue()
        self.resp_queue: Queue = Queue()

        # Keep track of child processes
        self.processes: List[Process] = []

    def _register_signals(self) -> None:
        signal.signal(signal.SIGINT, self._shutdown_signal_handler)
        signal.signal(signal.SIGTERM, self._shutdown_signal_handler)

    def _start_microlab(self) -> None:
        proc = Process(
            target=start_microlab_process,
            args=(self.cmd_queue, self.resp_queue, MultiprocessingLogger.get_logging_queue()),
            name='microlab',
        )
        self.processes.append(proc)
        self.logger.debug(self.t['starting-microlab-process'])
        proc.start()
        self.logger.debug(f'microlab process pid: {proc.pid}')

    def _start_server(self) -> None:
        proc = Process(
            target=start_flask_process,
            args=(self.cmd_queue, self.resp_queue, MultiprocessingLogger.get_logging_queue()),
            name='flask',
        )
        self.processes.append(proc)
        self.logger.debug(self.t['starting-server-process'])
        proc.start()
        self.logger.debug(f'server process pid: {proc.pid}')

    def _cleanup(self) -> None:
        self.logger.debug(self.t['begin-exit'])

        # 1) Notify workers to shut down
        for q in (self.cmd_queue, self.resp_queue):
            try:
                q.put(SHUTDOWN_SIGNAL)
            except Exception:
                self.logger.warning('Failed to send shutdown sentinel', exc_info=True)

        # 2) Join/terminate child processes
        for proc in self.processes:
            self.logger.debug(f'Joining process {proc.name} ({proc.pid})')
            proc.join(timeout=2)
            if proc.is_alive():
                self.logger.warning(f'{proc.name} did not exit; terminating')
                proc.terminate()
                proc.join()

        # 3) Clean up queues
        self.logger.debug(self.t['cleaning-queues'])
        for q in (self.cmd_queue, self.resp_queue):
            q.close()
            q.join_thread()
        self.logger.debug(self.t['cleaned-queues'])

        # 4) Flush remaining logs
        while MultiprocessingLogger.remaining_logs_to_process():
            MultiprocessingLogger.process_logs()

        self.logger.debug(self.t['completed-exit'])
        self.logger.debug(self.t['end-exit'])

    def _shutdown_signal_handler(self, signum: int, frame: Optional[FrameType]) -> None:
        self._cleanup()

    def run(self) -> None:
        # Perform any initial setup (e.g. hardware calibration, config file checks)
        config.initialSetup()

        # Register signal handlers before launching children
        self._register_signals()

        self.logger.info(self.t['starting-main-service'])

        # Launch worker processes
        self._start_microlab()
        self._start_server()

        # Block until all child processes exit
        for proc in self.processes:
            proc.join()

        # Ensure any remaining log messages are processed
        while MultiprocessingLogger.remaining_logs_to_process():
            MultiprocessingLogger.process_logs()


def main() -> None:
    # must initialize logger before any Queue()/Process() creations
    MultiprocessingLogger.initialize_logger()

    # Validate config early
    microlabConfig.validate_config()
    backend_manager = BackendManager()
    backend_manager.run()


if __name__ == '__main__':
    # Enforce *spawn* start method before any Queue is created
    set_start_method('spawn')
    main()
