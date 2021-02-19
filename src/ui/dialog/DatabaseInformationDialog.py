from PySide6.QtWidgets import QDialog

from src.__main__ import ROOT_DIR
from src.db.DBConnection import DBConnection
from src.ui import UiLoader


class DatabaseInformationDialog(QDialog):
    UI_FILE = ROOT_DIR + "/ui/DatabaseInformationDialog.ui"

    def __init__(self, parent=None):
        super(DatabaseInformationDialog, self).__init__(parent)
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        connection = DBConnection.instance()
        if connection:
            name = connection.query("SELECT Name FROM Metadata")[0][0]
            description = connection.query("SELECT Description FROM Metadata")[0][0]
            self.ui.nameLabel.setText(name)
            self.ui.descriptionLabel.setText(description)
