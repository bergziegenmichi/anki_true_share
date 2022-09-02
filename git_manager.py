from __future__ import annotations
from git import Repo


class GitManager:
    repo: Repo = None

    @staticmethod
    def init_repo(path: str, remote_url: str) -> GitManager:
        repo = Repo.init(path)
        repo.create_remote('origin', url=remote_url)
        return GitManager(path)

    def __init__(self, path: str):
        self.repo = Repo(path)

    def has_changes(self) -> bool:
        return self.repo.is_dirty(untracked_files=True)

    def push(self):
        self.repo.remotes.origin.push("main:main")

    def pull(self):
        self.repo.remotes.origin.pull("main:main")

    def add(self, files: list[str]):
        self.repo.index.add(files)

    def add_all(self):
        self.add(["*"])

    def commit(self, message: str):
        self.repo.index.commit(message)
