import logging
import logging.handlers
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

    @classmethod
    def initialize_logger(cls, logging_queue: Union[Queue, None] = None) -> None:
        """ Initialize the logger.

        Must be called in the base process that start the other processes without any argument.
        In other process it must be called with a dedicated logging queue."""
        if logging_queue is None:
            logging_queue = Queue()

        cls._logging_queue = logging_queue

    @classmethod
    def get_logging_queue(cls) -> Union[Queue, None]:
        return cls._logging_queue

    @classmethod
    def get_logger(cls, logger_name: str) -> logging.Logger:
        # We only need to configure once, multiple calls to logging.getLogger(<logger_name>)
        # will return the same configured instance
        if logger_name in cls._configured_loggers:
            return logging.getLogger(logger_name)

        logger = logging.getLogger(logger_name)
        logger.addHandler(logging.handlers.QueueHandler(cls._logging_queue))
        logger.setLevel(config.microlabConfig.logLevel)

        cls._configured_loggers[logger_name] = True

        return logger

    @classmethod
    def _get_processing_logger(cls, logger_name: str) -> logging.Logger:
        if logger_name in cls._configured_loggers:
            return logging.getLogger(logger_name)

        formatter = MultiLineFormatter(fmt="%(asctime)s %(name)-10s [%(levelname)s]: %(message)s")

        log_handlers = []

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

        cls._configured_loggers[logger_name] = True

        return logger

    @classmethod
    def remaining_logs_to_process(cls) -> bool:
        return cls._logging_queue.empty() == False

    @classmethod
    def process_logs(cls):
        try:
            record = cls._logging_queue.get_nowait()

            # We do the record.name against __main__ specifically so we can get the logger from the main thread
            # and not have it return the QueueHandler which not only causes issues but also means dropped logging
            # from the main thread
            if record.name == '__main__':
                logger = cls._get_processing_logger('main')
            else:
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


