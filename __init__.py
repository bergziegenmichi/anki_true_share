from aqt import mw
from aqt.qt import QAction

from .setup import setup
from .synchronizer import Synchronizer
from .widgets import ShareDeckWidget


def add_synced():
    mw.my_widget = ShareDeckWidget(synchronizer, mw.col.decks.all_names())


def sync_up():
    synchronizer.sync_all_decks()


def sync_down():
    synchronizer.sync_down()


setup()

synchronizer = Synchronizer()

menu = mw.form.menubar.addMenu("True Share")
action_add_synced = QAction("Share deck")
action_sync_up = QAction("Sync up (push)")
action_sync_down = QAction("Sync down (pull)")

action_add_synced.triggered.connect(add_synced)
action_sync_up.triggered.connect(sync_up)
action_sync_down.triggered.connect(sync_down)

menu.addActions([action_add_synced, action_sync_up, action_sync_down])
