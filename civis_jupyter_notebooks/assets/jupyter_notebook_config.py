"""Jupyter configuration file

Note that the code in this file gets executed in a python process that is independent
of any python process in a kernel run by Jupyter (e.g., an ipython kernel). Thus we can make
changes to the installed packages to use in the ipython kernel here without worrying about
them not being reimported.
"""
import os
import signal
import pip
from civis_jupyter_notebooks import platform_persistence
from civis_jupyter_notebooks.platform_persistence import NotebookManagementError

# Jupyter Configuration
c = get_config() # noqa
c.NotebookApp.ip = '*'
c.NotebookApp.allow_origin = '*'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.token = ''
c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': "frame-ancestors *"}}
c.MultiKernelManager.default_kernel_name = os.environ['DEFAULT_KERNEL']
c.NotebookApp.allow_root = True
c.FileContentsManager.post_save_hook = platform_persistence.post_save

git_enabled = os.environ.get('GIT_FILE') is not None

# File paths for notebook file and requirements.txt
REQUIREMENTS_PATH = os.path.expanduser(os.path.join('~', 'work', 'requirements.txt'))
NOTEBOOK_PATH = os.path.join('~', 'work', 'notebook.ipynb')
NOTEBOOK_PATH = os.path.expanduser(NOTEBOOK_PATH)

# Download notebook and initialize post-save hook
try:
    if not git_enabled or not os.path.isfile(NOTEBOOK_PATH):
        platform_persistence.initialize_notebook_from_platform(NOTEBOOK_PATH)

    # force a save of the preview so that we have one in case
    # the user never generates one
    _, preview_url = platform_persistence.get_update_urls()
    platform_persistence.generate_and_save_preview(preview_url, NOTEBOOK_PATH)
except NotebookManagementError as e:
    platform_persistence.logger.error(str(e))
    platform_persistence.logger.warn('Killing the notebook process b/c of a startup issue')
    os.kill(os.getpid(), signal.SIGTERM)

# Clone git repository
# Install requirements.txt
if os.path.isfile(REQUIREMENTS_PATH):
    platform_persistence.logger.info('installing requirements.txt packages')
    pip.main(['install', '-r', REQUIREMENTS_PATH])
    platform_persistence.logger.info('requirements.txt installed')
