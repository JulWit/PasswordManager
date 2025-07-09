import logging
from typing import Optional

from PySide6.QtCore import Signal, Slot, QMetaObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget

from src import ROOT_DIR
from src.ui import UiLoader
from src.ui.widget.PasswordGeneratorFrame import PasswordGeneratorFrame
from src.util.Theme import icon_path


class PasswordGeneratorWidget(QWidget):
    """
    Widget für das Generieren von Passwörtern.
    """

    # Ui-Datei
    UI_FILE = ROOT_DIR + "/ui/PasswordGeneratorWidget.ui"

    # Signal, dass entsandt wird, wenn der abbrechen-Button geklickt wurde.
    back = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues PasswortGeneratorWidget-Objekt.
        """
        super(PasswordGeneratorWidget, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self, {"PasswordGeneratorFrame": PasswordGeneratorFrame})


        # Setup Signal/Slots
        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_backButton_clicked(self) -> None:
        self.back.emit()
