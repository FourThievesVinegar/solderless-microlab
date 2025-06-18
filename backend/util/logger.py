import logging
import logging.handlers
import queue
import sys
import threading
import time
from multiprocessing import Queue
from os import path, makedirs
from typing import Optional

import config
from localization import load_translation
from util.log_formatter import MultiLineFormatter


class MultiprocessingLogger:
    """
    A singleton‐style logger that, in the "main" process, starts a background
    thread to drain a multiprocessing.Queue of LogRecords, replaying them through
    normal handlers (RotatingFileHandler, StreamHandler, etc.). Child processes
    simply get a "QueueHandler" pointed at that same queue.
    """

    _t: dict[str, str] = load_translation()

    # The shared multiprocessing Queue into which child processes will put LogRecords.
    _logging_queue: Optional[Queue] = None

    # A map from logger_name -> Logger object, so that the Loggers are configured once only.
    _configured_loggers: dict[str, logging.Logger] = {}

    # The dedicated "processing logger" (i.e. the one that actually writes to file/stderr) is referenced by this name.
    _processing_logger_name: str = '__mp_logger__'

    # Will hold the background Thread that calls process_logs() continuously.
    _processor_thread: Optional[threading.Thread] = None

    # Event to tell the background thread to exit
    _processor_stop_event: Optional[threading.Event] = None

    # Is this a "main" (i.e. the process that should drain the queue)? Set in initialize_logger().
    _is_main_process: bool = False

    @classmethod
    def initialize_logger(cls, logging_queue: Optional[Queue] = None) -> None:
        """
        Must be called *first* in every process that uses this class.
        - In the "main" process: call with no arguments. That sets _is_main_process=True,
          creates a new multiprocessing.Queue, and spins up the background thread.
        - In each child process: call with the Queue passed in from the main process. That sets
          _is_main_process=False, and simply remembers the queue so that any get_logger()
          calls return a QueueHandler-based Logger.

        Usage:
            # In the very beginning of the "backend/main.py":
            MultiprocessingLogger.initialize_logger()

            # Pass MultiprocessingLogger.get_logging_queue() into each child.
        """
        if logging_queue is None:
            # This is the main process
            cls._is_main_process = True
            cls._logging_queue = Queue()
            cls._start_processor_thread()
        else:
            # This is a worker process
            cls._is_main_process = False
            cls._logging_queue = logging_queue

    @classmethod
    def get_logging_queue(cls) -> Optional[Queue]:
        """
        Return the single multiprocessing.Queue used for all QueueHandlers.
        """
        return cls._logging_queue

    @classmethod
    def _start_processor_thread(cls) -> None:
        """
        Called only in the main process, right after creating the queue. Spins up
        a daemon thread that continuously calls process_logs() every 0.1s.
        We keep a stop-event `_processor_stop_event` to ask it to exit cleanly later.
        """
        if not cls._is_main_process or cls._logging_queue is None:
            return

        if cls._processor_thread is not None:
            # Already started
            return

        cls._processor_stop_event = threading.Event()

        def _processor_loop():
            while not cls._processor_stop_event.is_set():
                # Drain one record if available; if not, just return immediately.
                cls.process_logs()
                # Brief sleep to avoid spinning CPU at 100%
                time.sleep(0.1)

            # Once stop_event is set, do a final drain of anything left over.
            while cls.remaining_logs_to_process():
                cls.process_logs()

        thread = threading.Thread(
            target=_processor_loop,
            name='MultiprocessingLoggerProcessor',
            daemon=True,
        )
        thread.start()
        cls._processor_thread = thread

        # ensure that the "processing logger" entry is properly initialized
        cls._get_processing_logger(cls._processing_logger_name)

    @classmethod
    def stop_processing_thread(cls) -> None:
        """
        Called only in backend/main.py to cleanly exit. This will signal the
        background thread to stop, wait (join) up to 2s, and then do one last drain.
        """
        if cls._is_main_process and cls._processor_thread:
            cls._processor_stop_event.set()
            cls._processor_thread.join(timeout=2)

            # After join, do a final manual drain, in case anything snuck in:
            while cls.remaining_logs_to_process():
                cls.process_logs()

            cls._processor_thread = None
            cls._processor_stop_event = None

    @classmethod
    def _get_queue_logger(cls, logger_name: str) -> logging.Logger:
        """
        In a child process: return a Logger that has a QueueHandler, pointed at the shared multiprocessing Queue.
        """
        if logger_name in cls._configured_loggers:
            return cls._configured_loggers[logger_name]

        if cls._logging_queue is None:
            raise RuntimeError('MultiprocessingLogger not initialized with a queue!')

        logger = logging.getLogger(logger_name)
        q_handler = logging.handlers.QueueHandler(cls._logging_queue)
        logger.addHandler(q_handler)
        logger.setLevel(config.microlab_config.logLevel)
        cls._configured_loggers[logger_name] = logger
        return logger

    @classmethod
    def _get_processing_logger(cls, logger_name: str) -> logging.Logger:
        """
        In the main process: return (or create) a logger that writes to file/stderr.
        All dequeued records will be re-emitted through this logger.
        """
        if logger_name in cls._configured_loggers:
            return cls._configured_loggers[logger_name]

        formatter = MultiLineFormatter(
            fmt='%(asctime)s %(name)-10s [%(levelname)s]: %(message)s'
        )

        log_directory = config.microlab_config.logDirectory
        makedirs(log_directory, exist_ok=True)

        rotating_file_handler = logging.handlers.RotatingFileHandler(
            path.join(log_directory, 'microlab.log'),
            maxBytes=config.microlab_config.logFileMaxBytes,
            backupCount=config.microlab_config.logFileBackupCount,
        )
        rotating_file_handler.setFormatter(formatter)

        handlers: list[logging.Handler] = [rotating_file_handler]
        if config.microlab_config.logToStderr:
            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setFormatter(formatter)
            handlers.append(stderr_handler)

        # Create the logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(config.microlab_config.logLevel)
        for h in handlers:
            logger.addHandler(h)

        cls._configured_loggers[logger_name] = logger
        return logger

    @classmethod
    def get_logger(cls, logger_name: str) -> logging.Logger:
        """
        Public method to grab a Logger by name.
        - In child processes, returns a QueueHandler logger.
        - In main, returns a "processing" logger (writes to file/stderr).
        """
        if cls._is_main_process:
            # Always route everything through the same "processing logger" name,
            # to have only one set of file/stderr handlers.
            return cls._get_processing_logger(cls._processing_logger_name)
        else:
            return cls._get_queue_logger(logger_name)

    @classmethod
    def remaining_logs_to_process(cls) -> bool:
        """
        Returns True if there are still records in the multiprocessing Queue.
        """
        if cls._logging_queue is None:
            return False
        return not cls._logging_queue.empty()

    @classmethod
    def process_logs(cls) -> None:
        """
        Attempt to drain exactly one record (if present) from the queue, then
        re-emit it through the "processing logger."; If the queue is empty, return.
        """
        if cls._logging_queue is None:
            return

        try:
            record = cls._logging_queue.get_nowait()
        except queue.Empty:
            return
        except Exception as e:
            # In case of some unexpected error reading from queue
            sys.stderr.write(cls._t['log-exception'].format(e))
            sys.stderr.write('\n')
            return

        # Reconstruct or get the single "processing" logger, and handle
        processor = cls._get_processing_logger(cls._processing_logger_name)
        processor.handle(record)
