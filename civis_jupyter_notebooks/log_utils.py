import logging
import os
import sys

USER_LOGS_URL = '/edit/civis-notebook-logs.log'

USER_VISIBLE_LOGS = os.path.expanduser(os.path.join('~', 'work', 'civis-notebook-logs.log'))


def setup_stream_logging():
    """ Set up log format """
    logger = logging.getLogger('CIVIS_PLATFORM_BACKEND')
    logger.setLevel(logging.INFO)

    # prevents duplicate log records by preventing messages from being passed to ancestor loggers, i.e. the root logger
    logger.propagate = False

    formatter = logging.Formatter(
        fmt='[%(levelname).1s %(asctime)s %(name)s] %(message)s',
        datefmt="%H:%M:%S")
    error_handler = logging.StreamHandler(stream=sys.__stderr__)
    info_handler = logging.StreamHandler(stream=sys.__stdout__)

    error_handler.setLevel(logging.WARNING)
    info_handler.setLevel(logging.INFO)

    error_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)

    logger.addHandler(error_handler)
    logger.addHandler(info_handler)

    logger.info('hello! this is an info message')
    logger.warn('warning!')

    return logger


def setup_file_logging():
    directory = os.path.dirname(USER_VISIBLE_LOGS)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # python2 and 3 compatible way of opening a file
    open(USER_VISIBLE_LOGS, 'a').close()

    logger = logging.getLogger('USER_VISIBLE_LOGS')
    logger.setLevel(logging.ERROR)
    logger.propagate = False
    handler = logging.FileHandler(USER_VISIBLE_LOGS)
    formatter = logging.Formatter(
        fmt='[%(levelname).1s %(asctime)s %(name)s] %(message)s',
        datefmt="%H:%M:%S")
    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def log_file_has_logs(file_path):
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0
