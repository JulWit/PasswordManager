from PySide6.QtWidgets import QDialog

from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class AboutDialog(QDialog):
    UI_FILE = ROOT_DIR + "/ui/AboutDialog.ui"

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
