from typing import Optional

from PySide6.QtWidgets import QDialog, QWidget

from src import ROOT_DIR
from src.ui import UiLoader
from src.ui.widget.PasswordGeneratorFrame import PasswordGeneratorFrame
from src.util.Center import center_on_parent


class PasswordGeneratorDialog(QDialog):
    """
    Dialog für das Generieren von Passwörtern.
    """

    # UI-Datei
    UI_FILE = ROOT_DIR + "/ui/PasswordGeneratorDialog.ui"

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialisiert ein neues PasswordGeneratorDialog-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(PasswordGeneratorDialog, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self, {"PasswordGeneratorFrame": PasswordGeneratorFrame})

        # zentrieren
        center_on_parent(self)

    def password(self):
        return self.ui.passwordGeneratorFrame.password
