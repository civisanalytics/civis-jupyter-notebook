import unittest
import six
import pkg_resources
import platform

from civis_jupyter_notebooks.extensions.git.uncommitted_changes import UncommittedChangesHandler
from civis_jupyter_notebooks.git_utils import CivisGitError

if (six.PY2 or pkg_resources.parse_version('.'.join(platform.python_version_tuple()[0:2]))
        == pkg_resources.parse_version('3.4')):
    from mock import patch
    from mock import MagicMock
else:
    from unittest.mock import patch
    from unittest.mock import MagicMock


class UncommittedChangesHandlerTest(unittest.TestCase):

    def setUp(self):
        self.handler = UncommittedChangesHandler(MagicMock(), MagicMock())
        self.handler.finish = MagicMock()

    @patch('civis_jupyter_notebooks.extensions.git.uncommitted_changes.CivisGit')
    def test_get_will_return_404(self, civis_git):
        civis_git.return_value.is_git_enabled.return_value = False

        dummy_response = {'status': 404}
        self.handler.get()
        self.handler.finish.assert_called_with(dummy_response)

    @patch('civis_jupyter_notebooks.extensions.git.uncommitted_changes.CivisGit')
    def test_get_will_return_200(self, civis_git):
        civis_git.return_value.is_git_enabled.return_value = True
        civis_git.return_value.has_uncommitted_changes.return_value = True

        dummy_response = {'status': 200, 'has_uncommitted_changes': True}

        self.handler.get()
        civis_git.return_value.has_uncommitted_changes.assert_called()
        self.handler.finish.assert_called_with(dummy_response)

    @patch('civis_jupyter_notebooks.extensions.git.uncommitted_changes.CivisGit')
    def test_get_will_return_200_even_with_error(self, civis_git):
        civis_git.return_value.is_git_enabled.return_value = True
        civis_git.return_value.has_uncommitted_changes.side_effect = CivisGitError('dummy error')
        dummy_response = {'status': 200, 'has_uncommitted_changes': False}
        self.handler.get()
        self.handler.finish.assert_called_with(dummy_response)


if __name__ == '__main__':
    unittest.main()
