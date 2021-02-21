from typing import Optional

from PySide6.QtWidgets import QFrame, QWidget

from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class PasswordGeneratorFrame(QFrame):
    """
    Frame für das generieren von Passwörtern.
    """

    # UI-Datei
    UI_FILE = ROOT_DIR + "/ui/PasswordGeneratorFrame.ui"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues PasswordGeneratorFrame-Objekt.
        """
        super(PasswordGeneratorFrame, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
