import logging
from typing import Optional

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QWidget

from src.db.DBConnection import DBConnection
from src.db.Entry import Entry
from src.ui.widget.EntryWidget import EntryWidget


class NewEntryWidget(EntryWidget):

    entryCreated = Signal(Entry)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(NewEntryWidget, self).__init__(parent)

        # Setup logging
        self.logger = logging.getLogger("Logger")

        # Setup UI
        self.ui.headerLabel.setText("Neuer Eintrag:")
        self.ui.okButton.setEnabled(False)

    @Slot()
    def on_okButton_clicked(self) -> None:
        title = self.ui.titleLineEdit.text()
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        url = self.ui.urlLineEdit.text()
        notes = self.ui.notesTextEdit.toPlainText()

        self.entryCreated.emit(Entry(None, title, username, password, url, notes))
        self.ok.emit()
        self.clear()

    @Slot()
    def on_cancelButton_clicked(self) -> None:
        self.clear()
        self.cancel.emit()
