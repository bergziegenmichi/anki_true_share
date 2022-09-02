from aqt import mw


class ConfigManager:
    config: dict[str, dict[str, str]]
    module: str

    def __init__(self, module: str):
        self.module = module
        self.config = mw.addonManager.getConfig(module)

    def get_shared_decks(self) -> list[str]:
        return list(self.config["shared_decks"].keys())

    def get_deck_remote(self, name: str) -> str | None:
        for deck, remote in self.config["shared_decks"].items():
            if deck == name:
                return remote
        return None

    def add_shared_deck(self, name: str, remote: str):
        self.config["shared_decks"][name] = remote

    def write_config(self):
        mw.addonManager.writeConfig(self.module, self.config)
