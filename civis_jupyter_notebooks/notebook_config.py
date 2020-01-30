import json
import os
import signal

from civis_jupyter_notebooks import platform_persistence
from civis_jupyter_notebooks.git_utils import CivisGit


ROOT_DIR = os.path.expanduser(os.path.join('~', 'work'))


def get_notebook(notebook_full_path):
    try:
        platform_persistence.initialize_notebook_from_platform(notebook_full_path)
        platform_persistence.post_save({'type': 'notebook'}, notebook_full_path, None)
    except platform_persistence.NotebookManagementError as e:
        platform_persistence.logger.error(str(e))
        platform_persistence.logger.warn('Killing the notebook process b/c of a startup issue')
        os.kill(os.getpid(), signal.SIGTERM)


def find_and_install_requirements(requirements_path, c):
    try:
        platform_persistence.find_and_install_requirements(requirements_path)
    except platform_persistence.NotebookManagementError as e:
        error_msg = "Unable to install requirements.txt:\n" + str(e)
        platform_persistence.logger.error(error_msg)


def monkey_patch_jupyter_login_cookie():
    from http.cookies import Morsel
    from notebook.auth import login

    class PatchedLoginHandler(login.LoginHandler):
        @classmethod
        def set_login_cookie(cls, handler, user_id=None):
            """Call this on handlers to set the login cookie for success"""
            cookie_options = handler.settings.get('cookie_options', {})
            cookie_options.setdefault('httponly', True)
            cookie_options.setdefault('secure', True)
            cookie_options.setdefault('samesite', 'None')
            # tornado <4.2 has a bug that considers secure==True as soon as
            # 'secure' kwarg is passed to set_secure_cookie
            if handler.settings.get('secure_cookie', handler.request.protocol == 'https'):
                cookie_options.setdefault('secure', True)
            cookie_options.setdefault('path', handler.base_url)
            platform_persistence.logger.info(f'Cookie Options: {json.dumps(cookie_options)}')
            handler.set_secure_cookie(handler.cookie_name, user_id, **cookie_options)
            return user_id

    platform_persistence.logger.info('Monkey patching stuff')
    Morsel._reserved['samesite'] = 'SameSite'
    login.LoginHandler = PatchedLoginHandler


def config_jupyter(c):
    # Jupyter Configuration
    c.NotebookApp.ip = '0.0.0.0'
    c.NotebookApp.allow_origin = '*'
    c.NotebookApp.port = 8888
    c.NotebookApp.open_browser = False
    c.NotebookApp.token = ''
    # c.NotebookApp.disable_check_xsrf = True
    # monkeypatch Morsel to allow SameSite cookies (only in Python 3.8+)
    # Morsel._reserved['samesite'] = 'SameSite'
    # c.JupyterHub.tornado_settings["cookie_options"] = dict(secure=True)
    # c.JupyterHub.cookie_options = dict(secure=True)
    # monkey_patch_jupyter_login_cookie()
    c.NotebookApp.cookie_options = {'secure': True, 'samesite': 'None'}
    c.NotebookApp.tornado_settings = {
        'headers': {'Content-Security-Policy': "frame-ancestors *"},
        'secure_cookie': True,
        'cookie_options': {'secure': True, 'samesite': 'None'},
    }
    c.NotebookApp.terminado_settings = {'shell_command': ['bash']}
    c.NotebookApp.allow_root = True
    c.NotebookApp.nbserver_extensions = {
        'civis_jupyter_notebooks.extensions.git.uncommitted_changes': True
    }
    c.FileContentsManager.post_save_hook = platform_persistence.post_save
    c.MultiKernelManager.default_kernel_name = os.environ['DEFAULT_KERNEL']


def stage_new_notebook(notebook_file_path):
    civis_git = CivisGit()
    if civis_git.is_git_enabled():
        repo = civis_git.repo()
        repo.index.add([notebook_file_path])


def civis_setup(c):
    config_jupyter(c)

    nb_file_path = os.environ.get('NOTEBOOK_FILE_PATH', 'notebook.ipynb').strip('/')
    notebook_full_path = os.path.join(ROOT_DIR, nb_file_path)
    c.NotebookApp.default_url = '/notebooks/{}'.format(nb_file_path)

    get_notebook(notebook_full_path)
    stage_new_notebook(nb_file_path)

    requirements_path = os.path.dirname(notebook_full_path)
    find_and_install_requirements(requirements_path, c)
