from typing import Optional

from PySide6.QtWidgets import QDialog, QWidget

from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class AboutDialog(QDialog):
    """
    Über-Dialog mit Informationen über das Programm.
    """

    # UI-Datei
    UI_FILE = ROOT_DIR + "/ui/AboutDialog.ui"

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialisiert ein neues AboutDialog-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(AboutDialog, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
