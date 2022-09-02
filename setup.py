import os

from aqt import mw


class Defaults:
    config: str = '{"shared_decks":{}}'


def setup():
    path = mw.addonManager.addonsFolder(
        str(__name__).replace(".first_run", ""))

    os.makedirs(path + "/user_files", exist_ok=True)
    os.makedirs(path + "/user_files/git_repos", exist_ok=True)
    os.makedirs(path + "/user_files/symlinks", exist_ok=True)

    if not os.path.exists(path + "/config.json"):
        with open(path + "/config.json", "w") as f:
            f.write(Defaults.config)


