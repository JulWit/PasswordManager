from typing import Optional

from PySide6.QtWidgets import QDialog, QWidget

from src.__main__ import ROOT_DIR
from src.db.DBConnection import DBConnection
from src.ui import UiLoader


class DatabaseInformationDialog(QDialog):
    """
    Dialog der Metadaten über die Datenbank anzeigt.
    """

    # UI-Datei
    UI_FILE = ROOT_DIR + "/ui/DatabaseInformationDialog.ui"

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialisiert ein neues DatabaseInformationDialog-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(DatabaseInformationDialog, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        # Namen und Beschreibung der Datenbank auslesen
        connection = DBConnection.instance()
        if connection:
            name = connection.query("SELECT Name FROM Metadata")[0][0]
            description = connection.query("SELECT Description FROM Metadata")[0][0]
            self.ui.nameLabel.setText(name)
            self.ui.descriptionLabel.setText(description)
