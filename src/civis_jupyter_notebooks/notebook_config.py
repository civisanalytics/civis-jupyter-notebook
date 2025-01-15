import os
import signal

from civis_jupyter_notebooks import platform_persistence
from civis_jupyter_notebooks.git_utils import CivisGit

ROOT_DIR = os.path.expanduser(os.path.join("~", "work"))


def get_notebook(notebook_full_path):
    try:
        platform_persistence.initialize_notebook_from_platform(notebook_full_path)
        platform_persistence.post_save({"type": "notebook"}, notebook_full_path, None)
    except platform_persistence.NotebookManagementError as e:
        platform_persistence.logger.error(str(e))
        platform_persistence.logger.warn(
            "Killing the notebook process b/c of a startup issue"
        )
        os.kill(os.getpid(), signal.SIGTERM)


def find_and_install_requirements(requirements_path, c):
    try:
        platform_persistence.find_and_install_requirements(requirements_path)
    except platform_persistence.NotebookManagementError as e:
        error_msg = "Unable to install requirements.txt:\n" + str(e)
        platform_persistence.logger.error(error_msg)


def config_jupyter(c):
    # Jupyter Configuration
    c.ServerApp.ip = "0.0.0.0"  # nosec
    c.ServerApp.allow_origin = "*"
    c.ServerApp.root_dir = ROOT_DIR
    c.ServerApp.port = 8888
    c.ServerApp.open_browser = False
    # c.ServerApp.token = ""  # nosec
    c.IdentityProvider.token = ""  # nosec
    c.ServerApp.disable_check_xsrf = True
    c.ServerApp.allow_external_kernels = True
    c.ServerApp.tornado_settings = {
        "headers": {"Content-Security-Policy": "frame-ancestors *"}
    }
    c.ServerApp.terminado_settings = {"shell_command": ["bash"]}
    c.ServerApp.allow_root = True
    # c.NotebookApp.nbserver_extensions = {
    #     "civis_jupyter_notebooks.extensions.git.uncommitted_changes": True
    # }
    c.FileContentsManager.post_save_hook = platform_persistence.post_save
    c.MultiKernelManager.default_kernel_name = os.environ["DEFAULT_KERNEL"]

    # Install civis notebook v7 extension package
    package_path = os.path.join(
        os.path.dirname(__file__),
        "assets/extensions/civis_jupyter_notebook_extensions-0.1.0-py3-none-any.whl",
        # "assets/extensions/civis_jupyter_notebook-2.2.1-py3-none-any.whl",
    )
    os.system(f"pip install {package_path}")  # nosec


def stage_new_notebook(notebook_file_path):
    civis_git = CivisGit()
    if civis_git.is_git_enabled():
        repo = civis_git.repo()
        repo.index.add([notebook_file_path])


def civis_setup(c):
    config_jupyter(c)

    nb_file_path = os.environ.get("NOTEBOOK_FILE_PATH", "notebook.ipynb").strip("/")
    notebook_full_path = os.path.join(ROOT_DIR, nb_file_path)
    # c.NotebookApp.default_url = "/notebooks/{}".format(nb_file_path)
    # c.ServerApp.default_url = "/notebooks/{}".format(nb_file_path)
    c.ServerApp.default_url = "/doc/tree/{}".format(nb_file_path)
    # c.ServerApp.default_url = "/doc/workspaces/auto-s/tree/{}".format(nb_file_path)
    # c.LabApp.default_url = "/lab/tree/{}".format(nb_file_path)
    get_notebook(notebook_full_path)
    stage_new_notebook(nb_file_path)

    requirements_path = os.path.dirname(notebook_full_path)
    find_and_install_requirements(requirements_path, c)
