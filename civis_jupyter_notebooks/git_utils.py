import os
from git import Repo
from git.exc import GitCommandError


class CivisGit():
    def __init__(self, repo_url=None, repo_mount_path=None, git_repo_ref=None):
        self.repo_url = os.environ.get('GIT_REPO_URL', repo_url)
        self.git_repo_mount_path = repo_mount_path if repo_mount_path else os.path.expanduser(os.path.join('~', 'work'))
        self.git_repo_ref = os.environ.get('GIT_REPO_REF', git_repo_ref)

    def clone_repository(self):
        try:
            repo = Repo.clone_from(self.repo_url, self.git_repo_mount_path)
            repo.git.checkout(self.git_repo_ref)
        except GitCommandError as e:
            raise CivisGitError(e)

    def has_uncommitted_changes(self):
        try:
            repo = Repo(self.git_repo_mount_path)
            has_untracked_files = len(repo.untracked_files) > 0
            has_changes = len(repo.index.diff(None)) > 0
            return has_changes or has_untracked_files

        except GitCommandError as e:
            raise CivisGitError(e)


class CivisGitError(Exception):
    """
    General error raised whenever a Git related error comes up
    """
