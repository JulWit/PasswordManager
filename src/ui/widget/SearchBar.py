from typing import Optional

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLineEdit, QWidget

from src.__main__ import ROOT_DIR


class SearchBar(QLineEdit):
    """
    Suchleiste für das Durchsuchen einer TableView.
    """

    # UI-Datei
    ICON_FILE = ROOT_DIR + "/img/system-search.svg"

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Erstellt ein neues SearchBar-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(SearchBar, self).__init__(parent)
        self.setDisabled(True)
        self.setClearButtonEnabled(True)
        self.setClearButtonEnabled(True)
        self.setPlaceholderText("Einträge durchsuchen...")
        self.addAction(QIcon(self.ICON_FILE), QLineEdit.LeadingPosition)