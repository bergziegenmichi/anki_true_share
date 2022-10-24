from aqt.qt import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, \
    QRadioButton, QPushButton, QCheckBox, QHBoxLayout

from .synchronizer import Synchronizer


class ShareDeckWidget(QWidget):
    deck_select: QComboBox
    remote_url: QLineEdit
    push_button: QRadioButton
    pull_button: QRadioButton

    def __init__(self, synchronizer: Synchronizer, deck_names: list[str]):
        super().__init__()

        self.synchronizer = synchronizer

        self.init_me(deck_names)

    def init_me(self, deck_names: list[str]):
        self.setGeometry(400, 200, 500, 300)
        self.setFixedSize(self.size())

        layout = QVBoxLayout()

        deck_select_text = QLabel("Select deck to share")
        layout.addWidget(deck_select_text)
        self.deck_select = deck_select = QComboBox()
        deck_select.addItems(deck_names)
        layout.addWidget(deck_select)

        layout.addStretch(1)

        remote_url_text = QLabel("Enter the remote url")
        layout.addWidget(remote_url_text)
        self.remote_url = remote_url = QLineEdit()
        layout.addWidget(remote_url)

        layout.addStretch(1)

        push_pull_text = QLabel("Choose an action")
        layout.addWidget(push_pull_text)
        self.push_button = push_button = QRadioButton("push")
        push_button.setChecked(True)
        self.pull_button = pull_button = QRadioButton("pull")
        layout.addWidget(push_button)
        layout.addWidget(pull_button)

        layout.addStretch(1)

        ok_button = QPushButton("ok")

        ok_button.clicked.connect(self.process_input)
        layout.addWidget(ok_button)

        self.setLayout(layout)

        self.show()

    def process_input(self):
        deck = self.deck_select.currentText()
        remote_url = self.remote_url.text().strip()
        push = self.push_button.isChecked()
        pull = self.pull_button.isChecked()

        self.synchronizer.create_shared_deck(deck, remote_url, push, pull)

        self.close()


class SyncSpecificDecksWidget(QWidget):
    push_button: QRadioButton
    pull_button: QRadioButton
    checkboxes: list[QCheckBox]

    def __init__(self, synchronizer: Synchronizer, deck_names: list[str]):
        super().__init__()

        self.synchronizer = synchronizer

        self.init_me(deck_names)

    def init_me(self, deck_names: list[str]):
        layout = QVBoxLayout()

        deck_select_text = QLabel("Select deck(s) to sync")
        layout.addWidget(deck_select_text)

        self.checkboxes = []
        for deck_name in deck_names:
            checkbox = QCheckBox(deck_name)
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        layout.addStretch(1)

        push_pull_text = QLabel("Choose an action")
        layout.addWidget(push_pull_text)
        self.push_button = push_button = QRadioButton("push")
        push_button.setChecked(True)
        self.pull_button = pull_button = QRadioButton("pull")
        layout.addWidget(push_button)
        layout.addWidget(pull_button)

        layout.addStretch(1)

        sub_layout = QHBoxLayout()

        ok_button = QPushButton("ok")
        ok_button.clicked.connect(self.process_input)
        sub_layout.addWidget(ok_button)

        close_button = QPushButton("close")
        close_button.clicked.connect(self.close)
        sub_layout.addWidget(close_button)

        layout.addLayout(sub_layout)

        self.setLayout(layout)

        self.show()

    def process_input(self):
        checked = [checkbox.text() for checkbox in self.checkboxes
                   if checkbox.isChecked()]
        if self.pull_button.isChecked():
            self.synchronizer.sync_down_decks(checked)
        elif self.push_button.isChecked():
            self.synchronizer.sync_up_decks(checked)
