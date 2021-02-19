from typing import Optional

from PySide6.QtWidgets import QFrame, QWidget

from src.__main__ import ROOT_DIR
from src.db.Entry import Entry
from src.ui import UiLoader


class EntryDetailsFrame(QFrame):
    UI_FILE = ROOT_DIR + "/ui/EntryDetailsFrame.ui"

    def __init__(self, parent: Optional[QWidget] = None, entry: Optional[Entry] = None) -> None:
        super(EntryDetailsFrame, self).__init__(parent)

        self._entry = entry

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

    def update_entry_information(self, entry: Entry):
        self._entry = entry
        if entry is not None:
            self.ui.titleLabel.setText(entry.title)
            self.ui.usernameLabel.setText(entry.username)
            self.ui.passwordLabel.setText(entry.password)
            self.ui.urlLabel.setText(entry.url)
            self.ui.notesLabel.setText(entry.notes)
        else:
            self.ui.titleLabel.clear()
            self.ui.usernameLabel.clear()
            self.ui.passwordLabel.clear()
            self.ui.urlLabel.clear()
            self.ui.notesLabel.clear()
