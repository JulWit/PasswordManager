import logging
from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from src.__main__ import ROOT_DIR
from src.ui import UiLoader
from src.ui.widget.PasswordGeneratorFrame import PasswordGeneratorFrame


class PasswordGeneratorWidget(QWidget):
    """
    Widget für das generieren von Passwörtern
    """

    # Ui-Datei
    UI_FILE = ROOT_DIR + "/ui/PasswordGeneratorWidget.ui"

    # Signal, dass entsandt wird, wenn der abbrechen-Button geklickt wurde.
    cancel = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues PasswortGeneratorWidget-Objekt.
        """
        super(PasswordGeneratorWidget, self).__init__(parent)

        # Setup logging
        self.logger = logging.getLogger("Logger")

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self, {"PasswordGeneratorFrame": PasswordGeneratorFrame})
