from PySide6.QtWidgets import QMessageBox

from src.db.DBConnection import DBConnection


class DatabaseInformationMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super(DatabaseInformationMessageBox, self).__init__(parent)

        self.setWindowTitle("Datenbankinformationen anzeigen")
        self.setIcon(QMessageBox.Information)

        connection = DBConnection.instance()
        if connection:
            name = connection.query("SELECT Name FROM Metadata")
            description = connection.query("SELECT Description FROM Metadata")
            self.setText("Informationen über die Datenbank:")
            self.setInformativeText(f"Name: {name}\nBeschreibung: {description}\n")
