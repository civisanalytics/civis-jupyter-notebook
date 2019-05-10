import os
import civis
import logging
# from civis_jupyter_notebooks import log_utils

if 'CIVIS_API_KEY' in os.environ:
    LOGGER.info('creating civis api client')
    client = civis.APIClient(resources='all')
    LOGGER.info('civis api client created')


# Adapted from https://stackoverflow.com/a/1383365
class SingleLevelFilter(logging.Filter):
    def __init__(self, passlevel):
        self.passlevel = passlevel

    def filter(self, record):
        return (record.levelno == self.passlevel)


# Configure root logger for proper stream logging
root_logger = logging.getLogger()
# log_utils.configure_logger_for_stream_handling(root_logger)

root_logger.setLevel(logging.DEBUG)

# Configures a handler for sending warning level and above logs to stderr
error_handler = logging.StreamHandler(stream=sys.__stderr__)
error_handler.setLevel(logging.WARNING)
root_logger.addHandler(error_handler)

# Configures a handler for sending info level logs to stdout
info_handler = logging.StreamHandler(stream=sys.__stdout__)
info_handler.setLevel(logging.INFO)
# Filter so that the info handler will handle ONLY info level logs
info_handler.addFilter(SingleLevelFilter(logging.INFO))
root_logger.addHandler(info_handler)

root_logger.handlers = [error_handler, info_handler]

root_logger.info('root logger configured!')
root_logger.error('testing error messages on root logger')

# clean out the namespace for users
del os
