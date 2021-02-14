from PySide6.QtWidgets import QWidget

from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class EntryDetilsWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/EntryDetailsWidget.ui"

    def __init__(self, parent) -> None:
        super(EntryDetilsWidget, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
