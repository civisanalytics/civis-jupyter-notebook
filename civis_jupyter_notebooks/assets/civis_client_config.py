import os
import civis
import logging
from civis_jupyter_notebooks import log_utils

if 'CIVIS_API_KEY' in os.environ:
    LOGGER.info('creating civis api client')
    client = civis.APIClient(resources='all')
    LOGGER.info('civis api client created')

# Configure root logger for proper stream logging
root_logger = logging.getLogger()
log_utils.configure_logger_for_stream_handling(root_logger)

# clean out the namespace for users
del os
