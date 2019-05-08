import logging
import os
import sys

USER_LOGS_URL = '/edit/civis-notebook-logs.log'

USER_VISIBLE_LOGS = os.path.expanduser(os.path.join('~', 'work', 'civis-notebook-logs.log'))


# Adapted from https://stackoverflow.com/a/1383365
class SingleLevelFilter(logging.Filter):
    def __init__(self, passlevel):
        self.passlevel = passlevel

    def filter(self, record):
        return (record.levelno == self.passlevel)


def setup_stream_logging():
    """ Set up logging"""
    logger = logging.getLogger('CIVIS_PLATFORM_BACKEND')

    # prevents duplicate log records by preventing messages from being passed to ancestor loggers, i.e. the root logger
    logger.propagate = False

    # Sets the lowest level which this logger will pay attention to (i.e. debug level logs will be ignored)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt='[%(levelname).1s %(asctime)s %(name)s] %(message)s',
        datefmt="%H:%M:%S")

    # Configures a handler for sending warning level and above messages to stderr
    error_handler = logging.StreamHandler(stream=sys.__stderr__)
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    # Configures a handler for sending info level and above messages to stdout
    info_handler = logging.StreamHandler(stream=sys.__stdout__)
    # info_handler.setLevel(logging.INFO)
    # Filter so that the info handler will handle ONLY info level logs
    info_handler.addFilter(SingleLevelFilter(logging.INFO))
    info_handler.setFormatter(formatter)
    logger.addHandler(info_handler)

    # Test logs
    logger.debug('debug')
    logger.info('info')
    logger.warn('warn')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')

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

    logger.info('file logging info')
    logger.warn('file logging warn')
    logger.warning('file logging warning')
    logger.error('file logging error!')
    logger.critical('file logging critical!')
    return logger


def log_file_has_logs(file_path):
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0
