import os
from typing import Any

from aqt import mw

from .preferences import Preferences


def generate_default_config() -> dict[str, dict[str, str] | dict[Any]]:
    preferences = {"dupe_resolution": Preferences.DUPE_RESOLUTION.get_default()}
    config = {"shared_decks": {},
              "preferences": preferences}
    return config


def setup():
    path = mw.addonManager.addonsFolder(__name__.split(".")[0])

    os.makedirs(path + "/user_files", exist_ok=True)
    os.makedirs(path + "/user_files/git_repos", exist_ok=True)
    os.makedirs(path + "/user_files/symlinks", exist_ok=True)
