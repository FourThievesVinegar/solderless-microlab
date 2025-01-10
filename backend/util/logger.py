import logging
import logging.handlers
import os
import queue
import sys
import traceback

import config

from typing import Union
from multiprocessing import Queue
from util.logFormatter import MultiLineFormatter


class MultiprocessingLogger:

    _logging_queue = None
    _configured_loggers = {}

    _processing_logger = None

    _is_main_process = False

    @classmethod
    def initialize_logger(cls, logging_queue: Union[Queue, None] = None) -> None:
        """ Initialize the logger.

        Must be called in the base process that start the other processes without any argument.
        In other process it must be called with a dedicated logging queue."""
        if logging_queue is None:
            cls._is_main_process = True
            logging_queue = Queue()

        cls._logging_queue = logging_queue

    @classmethod
    def get_logging_queue(cls) -> Union[Queue, None]:
        return cls._logging_queue

    @classmethod
    def _get_queue_logger(cls, logger_name: str) -> logging.Logger:
        # We only need to configure once, multiple calls to logging.getLogger(<logger_name>)
        # will return the same configured instance
        if logger_name in cls._configured_loggers:
            return logging.getLogger(logger_name)

        logger = logging.getLogger(logger_name)
        logger.addHandler(logging.handlers.QueueHandler(cls._logging_queue))
        logger.setLevel(config.microlabConfig.logLevel)

        cls._configured_loggers[logger_name] = logger

        return logger

    @classmethod
    def get_logger(cls, logger_name: str) -> logging.Logger:
        if cls._is_main_process:
            return cls._get_processing_logger(logger_name)
        else:
            return cls._get_queue_logger(logger_name)

    @classmethod
    def _get_processing_logger(cls, logger_name: str) -> logging.Logger:
        if logger_name in cls._configured_loggers:
            return logging.getLogger(logger_name)

        formatter = MultiLineFormatter(fmt="%(asctime)s %(name)-10s [%(levelname)s]: %(message)s")

        log_handlers = []
        
        log_directory = config.microlabConfig.logDirectory        
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        rotating_file_handler = logging.handlers.RotatingFileHandler(
                "{0}/microlab.log".format(config.microlabConfig.logDirectory),
                maxBytes=config.microlabConfig.logFileMaxBytes,
                backupCount=config.microlabConfig.logFileBackupCount,
            )
        rotating_file_handler.setFormatter(formatter)
        log_handlers.append(rotating_file_handler)

        if config.microlabConfig.logToStderr:
            stderr_logger = logging.StreamHandler(sys.stderr)
            stderr_logger.setFormatter(formatter)
            log_handlers.append(stderr_logger)

        logger = logging.getLogger(logger_name)
        logger.setLevel(config.microlabConfig.logLevel)
        for handler in log_handlers:
            logger.addHandler(handler)

        cls._configured_loggers[logger_name] = logger

        return logger

    @classmethod
    def remaining_logs_to_process(cls) -> bool:
        return cls._logging_queue.empty() == False

    @classmethod
    def _does_logger_have_queue_handler(cls, logger: logging.Logger) -> bool:
        for handler in logger.handlers:
            if isinstance(handler, logging.handlers.QueueHandler):
                return True

    @classmethod
    def process_logs(cls):
        try:
            record = cls._logging_queue.get_nowait()
            logger = cls._get_processing_logger(record.name)
            logger.handle(record)
        except queue.Empty:
            return
        except ValueError as e:
            print(f'Value error: {e}')
            return
        except Exception as e:
            sys.stderr.write(f'Encountered exception: {e} while attempting to process logs. Traceback:\n')
            sys.stderr.write(traceback.format_exc())


