import logging
from typing import Optional

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QWidget

from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class UnlockDatabaseWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/PasswordGenerator.ui"

    cancel = Signal()

    def __init__(self, parent: Optional[QWidget] = None, file: str = None) -> None:
        super(UnlockDatabaseWidget, self).__init__(parent)
        self._file = file

        # Setup logging
        self.logger = logging.getLogger("Logger")

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)