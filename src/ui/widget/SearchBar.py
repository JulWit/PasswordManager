from typing import Optional

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLineEdit, QWidget

from src import ROOT_DIR
from src.util.Theme import icon_path


class SearchBar(QLineEdit):
    """
    Suchleiste für das Durchsuchen einer TableView.
    """

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
        self.addAction(QIcon(str(icon_path / "search.svg")), QLineEdit.ActionPosition.LeadingPosition)