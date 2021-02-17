from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from src.__main__ import ROOT_DIR
from src.db.Entry import Entry
from src.ui import UiLoader


class EntryDetailsWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/EntryDetailsWidget.ui"

    def __init__(self, parent: Optional[QWidget] = None, entry: Optional[Entry] = None) -> None:
        super(EntryDetailsWidget, self).__init__(parent)

        self._entry = entry

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

    @Slot(Entry)
    def update_entry_information(self, entry: Entry):
        self._entry = entry
