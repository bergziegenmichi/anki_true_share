import re

from aqt import mw


class Preference:
    def __init__(self):
        raise NotImplementedError


class _Preference(Preference):
    key: str
    default_value: str
    value_regex: str

    def __init__(self, key: str, default_value: str, value_regex: str = "*"):
        self.key = key
        self.default_value = default_value
        self.value_regex = value_regex

    def get(self) -> str:
        current = mw.addonManager.getConfig(__name__.split(".")[0])
        for subkey in self.key.split("."):
            current = current[subkey]
        return current

    def set(self, value: str) -> bool:
        if bool(re.match(self.value_regex, value)):
            config = mw.addonManager.getConfig(__name__.split(".")[0])
            current = config
            for subkey in self.key.split("."):
                current = current[subkey]
            current = value
            mw.addonManager.writeConfig(__name__.split(".")[0], config)
            return True
        return False

    def get_default(self) -> str:
        return self.default_value

    def set_default(self) -> bool:
        return self.set(self.default_value)


class SharedDecks:
    @staticmethod
    def get() -> dict[str, str]:
        return mw.addonManager.getConfig(
            __name__.split(".")[0])["shared_decks"]

    @staticmethod
    def get_names() -> list[str]:
        return list(SharedDecks.get().keys())

    @staticmethod
    def get_remote_urls() -> list[str]:
        return list(SharedDecks.get().values())

    @staticmethod
    def add(name: str, remote_url: str) -> bool:
        config = mw.addonManager.getConfig(__name__.split(".")[0])
        if name not in config["shared_decks"].keys():
            config["shared_decks"][name] = remote_url
            mw.addonManager.writeConfig(__name__.split(".")[0], config)
            return True
        return False

    @staticmethod
    def change(name: str, remote_url: str) -> bool:
        config = mw.addonManager.getConfig(__name__.split(".")[0])
        if name in config["shared_decks"].keys():
            config["shared_decks"][name] = remote_url
            mw.addonManager.writeConfig(__name__.split(".")[0], config)
            return True
        return False

    @staticmethod
    def delete(name: str) -> bool:
        config = mw.addonManager.getConfig(__name__.split(".")[0])
        if name in config["shared_decks"].keys():
            del config["shared_decks"][name]
            mw.addonManager.writeConfig(__name__.split(".")[0], config)
            return True
        return False


class Preferences:
    DUPE_RESOLUTION = _Preference("preferences.dupe_resolution", "update")
