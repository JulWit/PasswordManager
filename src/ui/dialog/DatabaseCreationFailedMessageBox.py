from typing import Optional

from PySide6.QtWidgets import QMessageBox, QWidget


class DatabaseCreationFailedMessageBox(QMessageBox):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(DatabaseCreationFailedMessageBox, self).__init__(parent)

        self.setWindowTitle("Datenbankerstllung fehlgeschlagen")
        self.setText("Die Datenbank konnte nicht erstellt werden")
        self.setIcon(QMessageBox.Critical)
