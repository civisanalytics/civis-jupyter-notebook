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
    """
    Configure the CIVIS_PLATFORM_BACKEND logger for stream logging.

    DEBUG level logs will be ignored,
    INFO level logs will be sent to stdout,
    WARNING, ERROR, & CRITICAL level logs will be sent to stderr.

    Returns
    -------
    The CIVIS_PLATFORM_BACKEND logger
    """
    logger = logging.getLogger('CIVIS_PLATFORM_BACKEND')

    # prevents duplicate log records by preventing messages from being passed to ancestor loggers, e.g. the root logger
    logger.propagate = False

    # Sets the lowest level which this logger will pay attention to (i.e. ignore debug level logs)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt='[%(levelname).1s %(asctime)s %(name)s] %(message)s',
        datefmt="%H:%M:%S")

    # Configures a handler for sending warning level and above logs to stderr
    error_handler = logging.StreamHandler(stream=sys.__stderr__)
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    # Configures a handler for sending info level logs to stdout
    info_handler = logging.StreamHandler(stream=sys.__stdout__)
    info_handler.setLevel(logging.INFO)
    # Filter so that the info handler will handle ONLY info level logs
    info_handler.addFilter(SingleLevelFilter(logging.INFO))
    info_handler.setFormatter(formatter)
    logger.addHandler(info_handler)

    return logger


def setup_file_logging():
    """
    Configure the USER_VISIBLE_LOGS for file logging.

    File logging is intended for errors to be shown to the user.
    E.g. If we fail to install requirements, then we redirect
    c.NotebookApp.default_url to point to this log file.

    TODO: This was written during the intial development
    of notebooks and may no longer be necessary. CIVP-18444

    Returns
    -------
    The USER_VISIBLE_LOGS logger
    """
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
