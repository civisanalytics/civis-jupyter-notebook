import os
import civis
from civis_jupyter_notebooks.platform_persistence import logger as LOGGER
from civis_jupyter_notebooks.notebook_config import monkey_patch_jupyter_login_cookie

if 'CIVIS_API_KEY' in os.environ:
    LOGGER.info('creating civis api client')
    client = civis.APIClient(resources='all')
    LOGGER.info('civis api client created')

monkey_patch_jupyter_login_cookie()

# clean out the namespace for users
del monkey_patch_jupyter_login_cookie
del os
del LOGGER
