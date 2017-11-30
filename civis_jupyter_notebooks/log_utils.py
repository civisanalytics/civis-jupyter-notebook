import logging
import os
import sys

USER_LOGS_FILE = '/root/work/logs/errors.log'


def setup_stream_logging():
    """ Set up log format """
    logger = logging.getLogger('CIVIS_PLATFORM_BACKEND')
    logger.setLevel(logging.INFO)
    # needed to remove duplicate log records..don't know why...
    logger.propagate = False
    # make sure to grab orig stderr since things seem to get redirected a bit
    # by the notebook and/or ipython...
    ch = logging.StreamHandler(stream=sys.__stderr__)
    formatter = logging.Formatter(
        fmt='[%(levelname).1s %(asctime)s %(name)s] %(message)s',
        datefmt="%H:%M:%S")
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def setup_file_logging():
    directory = os.path.dirname(USER_LOGS_FILE)
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        open(USER_LOGS_FILE, 'x')
    except FileExistsError:
        pass

    logger = logging.getLogger('USER_ERROR_LOGS')
    logger.setLevel(logging.ERROR)
    logger.propagate = False
    handler = logging.FileHandler(USER_LOGS_FILE)
    formatter = logging.Formatter(
        fmt='[%(levelname).1s %(asctime)s %(name)s] %(message)s',
        datefmt="%H:%M:%S")
    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
