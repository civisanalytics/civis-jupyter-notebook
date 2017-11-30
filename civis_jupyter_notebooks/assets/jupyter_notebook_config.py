"""Jupyter configuration file

Note that the code in this file gets executed in a python process that is independent
of any python process in a kernel run by Jupyter (e.g., an ipython kernel). Thus we can make
changes to the installed packages to use in the ipython kernel here without worrying about
them not being reimported.
"""
import os
import signal
import pip
from civis_jupyter_notebooks import platform_persistence, log_utils
from civis_jupyter_notebooks.platform_persistence import NotebookManagementError

# Jupyter Configuration
c = get_config() # noqa
c.NotebookApp.ip = '*'
c.NotebookApp.allow_origin = '*'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.token = ''
c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': "frame-ancestors *"}}
c.NotebookApp.allow_root = True
c.FileContentsManager.post_save_hook = platform_persistence.post_save
c.MultiKernelManager.default_kernel_name = os.environ['DEFAULT_KERNEL']

NOTEBOOK_PATH = os.path.expanduser(os.path.join('~', 'work'))
REQUIREMENTS_PATH = os.path.expanduser(os.path.join('~', 'work'))

if log_utils.log_file_has_logs(log_utils.USER_VISIBLE_LOGS):
    # redirect to log file
    c.NotebookApp.default_url = '/edit/civis-notebook-logs.log'
    platform_persistence.logger.info('user visible error log file has an entry')

else:
    nb_file_path = os.environ.get('NOTEBOOK_FILE_PATH')
    if nb_file_path:
        nb_file_path = nb_file_path.strip('/')
        NOTEBOOK_PATH = os.path.join(NOTEBOOK_PATH, nb_file_path)
        c.NotebookApp.default_url = '/notebooks/{}'.format(nb_file_path)
    else:
        NOTEBOOK_PATH = os.path.join(NOTEBOOK_PATH, 'notebook.ipynb')
        c.NotebookApp.default_url = '/notebooks/notebook.ipynb'

    try:
        # pull .ipynb file from s3 and save preview back if necessary
        # pull requirements.txt file from s3
        if not os.path.isfile(NOTEBOOK_PATH):
            platform_persistence.initialize_notebook_from_platform(NOTEBOOK_PATH)

        _, preview_url = platform_persistence.get_update_urls()
        platform_persistence.generate_and_save_preview(preview_url, NOTEBOOK_PATH)

    except NotebookManagementError as e:
        platform_persistence.logger.error(str(e))
        platform_persistence.logger.warn('Killing the notebook process b/c of a startup issue')
        os.kill(os.getpid(), signal.SIGTERM)

    # Install requirements.txt
    REQUIREMENTS_PATH = os.path.join(REQUIREMENTS_PATH, 'requirements.txt')
    if os.path.isfile(REQUIREMENTS_PATH):
        platform_persistence.logger.info('installing requirements.txt packages')
        pip.main(['install', '-r', REQUIREMENTS_PATH])
        platform_persistence.logger.info('requirements.txt installed')
