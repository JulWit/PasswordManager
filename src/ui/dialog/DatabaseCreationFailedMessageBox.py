from PySide6.QtWidgets import QMessageBox


class DatabaseCreationFailedMessageBox(QMessageBox):
    def __init__(self, parent=None) -> None:
        super(DatabaseCreationFailedMessageBox, self).__init__(parent)

        self.setWindowTitle("Datenbankerstllung fehlgeschlagen")
        self.setText("Die Datenbank konnte nicht erstellt werden")
