import os

from aqt import mw, gui_hooks

from .git_manager import GitManager
from .config_manager import ConfigManager
from .import_export import export_to_csv, import_from_csv


class Synchronizer:
    git_managers: dict[str, GitManager] = {}
    config_manager: ConfigManager
    user_files_folder: str

    def __init__(self, module_name: str):
        self.config_manager = ConfigManager(module_name)
        self.user_files_folder = mw.addonManager.addonsFolder(
            module_name) + "/user_files"

        self.git_managers = self.load_shared_decks()

        gui_hooks.collection_did_load.append(lambda x: self.sync_down())

        gui_hooks.sync_did_finish.append(self.sync_all_decks)

    def sync_all_decks(self):
        for deck_name in self.git_managers.keys():
            self.sync_deck(deck_name)
        self.config_manager.write_config()

    def sync_deck(self, deck_name):
        export_to_csv(deck_name, self.create_csv_path(deck_name))
        git_manager = self.git_managers[deck_name]
        git_manager.add_all()
        if git_manager.has_changes():
            # TODO
            git_manager.commit("der scheiß ghört noch geändert")
            git_manager.push()

    def sync_down(self):
        self.pull_all()
        for file in os.listdir(self.user_files_folder + "/symlinks"):
            import_from_csv(self.create_csv_path(file))

    def create_csv_path(self, deck_name):
        return f"{self.user_files_folder}/git_repos/{deck_name}/" \
               f"{deck_name}.csv"

    def load_shared_decks(self) -> dict[str, GitManager]:
        git_managers = {}
        for deck_name in self.config_manager.get_shared_decks():
            git_managers[deck_name] = GitManager(
                f"{self.user_files_folder}/git_repos/{deck_name}")
        return git_managers

    def create_shared_deck(self, deck_name: str, remote_url: str,
                           push: bool = True, pull: bool = False):

        if push + pull != 1:
            raise Exception

        self.config_manager.add_shared_deck(deck_name, remote_url)
        self.config_manager.write_config()
        git_path = f"{self.user_files_folder}/" \
                   f"git_repos/" \
                   f"{deck_name}/"
        git_manager = GitManager.init_repo(git_path, remote_url)
        self.git_managers[deck_name] = git_manager

        if push:
            output_path = export_to_csv(deck_name,
                                        self.create_csv_path(deck_name))
            os.symlink(output_path, f"{self.user_files_folder}/symlinks/"
                                    f"{deck_name}")
            git_manager.add_all()
            # TODO
            git_manager.commit("da ghört noch was gscheites her oida")
            git_manager.push()

        elif pull:
            git_manager.pull()
            import_path = self.create_csv_path(deck_name)
            os.symlink(import_path, f"{self.user_files_folder}/symlinks/"
                                    f"{deck_name}")
            import_from_csv(import_path)

    def push_all(self):
        for git_manager in self.git_managers.values():
            git_manager.push()

    def pull_all(self):
        for git_manager in self.git_managers.values():
            git_manager.pull()

    def push_specific(self, deck_name):
        self.git_managers[deck_name].push()

    def pull_specific(self, deck_name):
        self.git_managers[deck_name].pull()
