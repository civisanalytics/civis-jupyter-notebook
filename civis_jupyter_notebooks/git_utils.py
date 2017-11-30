import os
from git import Repo
from git.exc import GitCommandError


class CivisGit():
    def __init__(self):
        self.repo_url = os.environ.get('GIT_REPO_URL')
        self.git_repo_mount_path = os.path.expanduser(os.path.join('~', 'work'))
        self.git_repo_ref = os.environ.get('GIT_REPO_REF')

    def clone_repository(self):
        try:
            repo = Repo.clone_from(self.repo_url, self.git_repo_mount_path)
            repo.git.checkout(self.git_repo_ref)
        except GitCommandError as e:
            raise GitError(e)


class GitError(Exception):
    '''
    General error raised whenever a Git related error comes up
    '''
