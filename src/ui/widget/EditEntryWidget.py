import logging
from datetime import datetime
from typing import Optional

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QWidget

from src.db.Entry import Entry
from src.ui.widget.EntryWidget import EntryWidget


class EditEntryWidget(EntryWidget):

    edited = Signal(Entry)

    def __init__(self, entry: Entry, parent: Optional[QWidget] = None) -> None:
        super(EditEntryWidget, self).__init__(parent)

        self._entry = entry

        # Setup logging
        self.logger = logging.getLogger("Logger")

        # Setup UI
        self.ui.headerLabel.setText("Eintrag bearbeiten:")
        self.ui.titleLineEdit.setText(entry.title)
        self.ui.usernameLineEdit.setText(entry.username)
        self.ui.passwordLineEdit.setText(entry.password)
        self.ui.urlLineEdit.setText(entry.url)
        self.ui.notesTextEdit.setPlainText(entry.notes)

    @Slot()
    def on_okButton_clicked(self) -> None:
        self._entry.title = self.ui.titleLineEdit.text()
        self._entry.username = self.ui.usernameLineEdit.text()
        self._entry.password = self.ui.passwordLineEdit.text()
        self._entry.url = self.ui.urlLineEdit.text()
        self._entry.notes = self.ui.notesTextEdit.toPlainText()
        self._entry.modified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.edited.emit(self._entry)
        self.ok.emit()

    @Slot()
    def on_cancelButton_clicked(self) -> None:
        self.cancel.emit()
