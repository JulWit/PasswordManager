import logging

from PySide6.QtCore import Slot
from src.db.DBConnection import DBConnection
from src.ui.widget.EntryWidget import EntryWidget


class NewEntryWidget(EntryWidget):
    def __init__(self, parent=None):
        super(NewEntryWidget, self).__init__(parent)

        # Setup logging
        self.logger = logging.getLogger("Logger")

        # Setup UI
        self.ui.headerLabel.setText(self.tr("Neuer Eintrag:"))
        self.ui.okButton.setEnabled(False)

    @Slot()
    def on_okButton_clicked(self):
        title = self.ui.titleLineEdit.text()
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        url = self.ui.urlLineEdit.text()
        notes = self.ui.notesTextEdit.toPlainText()

        self.clear()

        query = "INSERT INTO Entries  (title, username, password, url, notes) VALUES (?, ?, ?, ?, ?)"
        connection = DBConnection()
        connection.execute(query, (title, username, password, url, notes))
        connection.commit()

        self.ok.emit()

    @Slot()
    def on_cancelButton_clicked(self):
        self.clear()
        self.cancel.emit()
