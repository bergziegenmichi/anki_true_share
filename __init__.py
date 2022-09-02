from aqt import mw
from aqt.qt import QAction
from .anki_true_sync import Synchronizer
from .setup import setup
from .widgets import AddSyncedDeckWidget


def add_synced():
    mw.my_widget = AddSyncedDeckWidget(synchronizer, mw.col.decks.all_names())


def sync_up():
    synchronizer.sync_all_decks()


def sync_down():
    synchronizer.sync_down()

setup()

synchronizer = Synchronizer(__name__)

menu = mw.form.menubar.addMenu("True Sync")
action_add_synced = QAction("add synced deck")
action_sync_up = QAction("sync up")
action_sync_down = QAction("sync down")

action_add_synced.triggered.connect(add_synced)
action_sync_up.triggered.connect(sync_up)
action_sync_down.triggered.connect(sync_down)

menu.addActions([action_add_synced, action_sync_up, action_sync_down])
