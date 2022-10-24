import os

from aqt import mw, gui_hooks

from .git_manager import GitManager
from .import_export import export_to_csv, import_from_csv
from .preferences import SharedDecks


class Synchronizer:
    git_managers: dict[str, GitManager] = {}
    user_files_folder: str

    def __init__(self, ):
        self.user_files_folder = mw.addonManager.addonsFolder(
            __name__.split(".")[0]) + "/user_files"

        self.git_managers = self.load_shared_decks()

        gui_hooks.collection_did_load.append(lambda x: self.sync_down_all())
        # otherwise passes collection as function parameter

        gui_hooks.sync_did_finish.append(self.sync_up_all)

    def sync_up_deck(self, name: str):
        export_to_csv(name, self.csv_path_from_name(name))
        git_manager = self.git_managers[name]
        git_manager.add_all()
        if git_manager.has_changes():
            # TODO actual commit message
            git_manager.commit("lulu")
            git_manager.push()

    def sync_up_decks(self, names: list[str]):
        for name in names:
            self.sync_up_deck(name)

    def sync_up_all(self):
        self.sync_up_decks(SharedDecks.get_names())

    def sync_down_deck(self, name: str):
        self.git_managers[name].pull()
        import_from_csv(self.csv_path_from_name(name))

    def sync_down_decks(self, names: list[str]):
        for name in names:
            self.sync_down_deck(name)

    def sync_down_all(self):
        self.sync_down_decks(SharedDecks.get_names())

    def csv_path_from_name(self, deck_name):
        return f"{self.user_files_folder}/git_repos/{deck_name}/" \
               f"{deck_name}.csv"

    def load_shared_decks(self) -> dict[str, GitManager]:
        git_managers = {}
        for deck_name in SharedDecks.get_names():
            git_managers[deck_name] = GitManager(
                f"{self.user_files_folder}/git_repos/{deck_name}")
        return git_managers

    def create_shared_deck(self, deck_name: str, remote_url: str,
                           push: bool = True, pull: bool = False):

        if push + pull != 1:
            raise Exception

        SharedDecks.add(deck_name, remote_url)
        git_path = f"{self.user_files_folder}/" \
                   f"git_repos/" \
                   f"{deck_name}/"
        git_manager = GitManager.init_repo(git_path, remote_url)
        self.git_managers[deck_name] = git_manager

        if push:
            output_path = export_to_csv(deck_name,
                                        self.csv_path_from_name(deck_name))
            git_manager.add_all()
            # TODO
            git_manager.commit("da ghört noch was gscheites her oida")
            git_manager.push()

        elif pull:
            git_manager.pull()
            import_path = self.csv_path_from_name(deck_name)
            import_from_csv(import_path)
