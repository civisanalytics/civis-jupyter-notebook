"""Jupyter configuration file

Note that the code in this file gets executed in a python process that is independent
of any python process in a kernel run by Jupyter (e.g., an ipython kernel). Thus we can make
changes to the installed packages to use in the ipython kernel here without worrying about
them not being reimported.
"""
import os
import signal
import sys
import subprocess
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

ROOT_DIR = os.path.expanduser(os.path.join('~', 'work'))
LOG_URL = '/edit/civis-notebook-logs.log'

if log_utils.log_file_has_logs(log_utils.USER_VISIBLE_LOGS):
    # redirect to log file
    c.NotebookApp.default_url = LOG_URL
else:
    nb_file_path = os.environ.get('NOTEBOOK_FILE_PATH', 'notebook.ipynb').strip('/')
    notebook_full_path = os.path.join(ROOT_DIR, nb_file_path)
    c.NotebookApp.default_url = '/notebooks/{}'.format(nb_file_path)

    try:
        # pull .ipynb and requirements.txt file from s3
        if not os.path.isfile(notebook_full_path):
            platform_persistence.initialize_notebook_from_platform(notebook_full_path)

        # save preview back if necessary
        _, preview_url = platform_persistence.get_update_urls()
        platform_persistence.generate_and_save_preview(preview_url, notebook_full_path)

    except NotebookManagementError as e:
        platform_persistence.logger.error(str(e))
        platform_persistence.logger.warn('Killing the notebook process b/c of a startup issue')
        os.kill(os.getpid(), signal.SIGTERM)

    # Install requirements.txt
    requirements_path = os.path.dirname(notebook_full_path)
    while os.path.isdir(requirements_path):
        requirements_file = os.path.join(requirements_path, 'requirements.txt')
        platform_persistence.logger.info('Looking for requirements at %s' % requirements_file)
        if os.path.isfile(requirements_file):
            platform_persistence.logger.info('Installing packages from %s' % requirements_file)
            try:
                subprocess.check_output(
                        [sys.executable, '-m', 'pip', 'install', '-r', requirements_file],
                        stderr=subprocess.STDOUT
                        )
                platform_persistence.logger.info('requirements.txt installed')
            except subprocess.CalledProcessError as e:
                # redirect to log file if pip fails
                error_msg = "Unable to install requirements.txt, error code %d:\n" % (e.returncode) + \
                    e.output.decode("utf-8")
                platform_persistence.logger.info(error_msg)
                with open(os.path.join(ROOT_DIR, 'civis-notebook-logs.log'), 'w') as f:
                    f.write(error_msg)
                platform_persistence.logger.info('Setting NotebookApp.default_url to %s' % LOG_URL)
                c.NotebookApp.default_url = LOG_URL
            break

        else:
            requirements_path = os.path.dirname(requirements_path)
