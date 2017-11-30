import unittest
import os
import logging
import six
import pkg_resources
import platform

from git.exc import GitCommandError
from git import Repo
from civis_jupyter_notebooks.git_utils import CivisGit, GitError

if (six.PY2 or pkg_resources.parse_version('.'.join(platform.python_version_tuple()[0:2]))
        == pkg_resources.parse_version('3.4')):
    from mock import patch
    from mock import MagicMock
else:
    from unittest.mock import patch
    from unittest.mock import MagicMock

REPO_URL = 'http://www.github.com/civisanalytics.foo.git'
GIT_REPO_REF = 'master'


class GitUtilsTest(unittest.TestCase):

    def setUp(self):
        os.environ['GIT_REPO_URL'] = REPO_URL
        os.environ['GIT_REPO_REF'] = GIT_REPO_REF
        logging.disable(logging.INFO)

    @patch('civis_jupyter_notebooks.git_utils.Repo.clone_from')
    def test_clone_repository_throws_error(self, repo_clone):
        repo_clone.side_effect = GitCommandError('clone', 'failed')
        self.assertRaises(GitError, lambda: CivisGit().clone_repository())

    @patch('civis_jupyter_notebooks.git_utils.Repo.clone_from')
    def test_clone_repository_succeeds(self, repo_clone):
        repo_clone.return_value = MagicMock(spec=Repo)
        CivisGit().clone_repository()

        repo_mount_path = '/root/work/'
        repo_clone.assert_called_with(REPO_URL, repo_mount_path)
        repo_clone.return_value.git.checkout.assert_called_with(GIT_REPO_REF)


if __name__ == '__main__':
    unittest.main()
