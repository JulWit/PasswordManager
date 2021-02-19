from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLineEdit

from src.__main__ import ROOT_DIR


class SearchBar(QLineEdit):

    ICON_FILE = ROOT_DIR + "/img/system-search.svg"

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDisabled(True)
        self.setClearButtonEnabled(True)
        self.setClearButtonEnabled(True)
        self.setPlaceholderText("Einträge durchsuchen...")
        self.addAction(QIcon(self.ICON_FILE), QLineEdit.LeadingPosition)

        # TODO: Padding?
