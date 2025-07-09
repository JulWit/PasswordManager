from typing import Optional

from PySide6.QtWidgets import QMessageBox, QWidget


class DatabaseCreationFailedMessageBox(QMessageBox):
    """
    MessageBox, die den Benutzer darüber informiert, dass die Datenbank nicht erstellt werden konnte.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues DatabaseCreationFailedMessageBox-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(DatabaseCreationFailedMessageBox, self).__init__(parent)
        self.setWindowTitle("Datenbankerstellung fehlgeschlagen")
        self.setText("Die Datenbank konnte nicht erstellt werden")
        self.setIcon(QMessageBox.Icon.Critical)
