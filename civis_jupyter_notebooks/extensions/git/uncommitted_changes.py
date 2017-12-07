from notebook.utils import url_path_join as ujoin
from tornado.web import RequestHandler
from civis_jupyter_notebooks.git_utils import CivisGit, CivisGitError


class UncommittedChangesHandler(RequestHandler):
    def get(self):
        response = dict()
        civis_git = CivisGit()

        if not civis_git.is_git_enabled():
            response['status'] = 404
        else:
            has_changes = False
            try:
                has_changes = civis_git.has_uncommitted_changes()
            except CivisGitError:
                pass

            response['status'] = 200
            response['has_uncommitted_changes'] = has_changes
        self.finish(response)


def load_jupyter_server_extension(nbapp):
    nbapp.log.info('Uncommitted Changes Ext. Loaded')

    webapp = nbapp.web_app
    base_url = webapp.settings['base_url']
    webapp.add_handlers(".*$", [
        (ujoin(base_url, r"/git/uncommitted_changes"), UncommittedChangesHandler),
    ])
