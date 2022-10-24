from aqt import mw
from aqt.qt import QAction

from .preferences import SharedDecks
from .setup import setup
from .synchronizer import Synchronizer
from .widgets import ShareDeckWidget, SyncSpecificDecksWidget


def add_synced():
    not_shared_decks = [deck_name for deck_name in mw.col.decks.all_names()
                        if deck_name not in SharedDecks.get_names()]
    mw.my_widget = ShareDeckWidget(synchronizer, not_shared_decks)


def sync_up():
    synchronizer.sync_up_all()


def sync_down():
    synchronizer.sync_down_all()


def sync_menu():
    mw.my_widget = SyncSpecificDecksWidget(synchronizer, SharedDecks.get_names())


setup()

synchronizer = Synchronizer()

menu = mw.form.menubar.addMenu("True Share")
action_add_synced = QAction("Share deck")
action_sync_up = QAction("Sync up (push)")
action_sync_down = QAction("Sync down (pull)")
action_sync_menu = QAction("Sync menu")

action_add_synced.triggered.connect(add_synced)
action_sync_up.triggered.connect(sync_up)
action_sync_down.triggered.connect(sync_down)
action_sync_menu.triggered.connect(sync_menu)

menu.addActions([action_add_synced, action_sync_up, action_sync_down, action_sync_menu])
