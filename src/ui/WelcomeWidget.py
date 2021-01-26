from PySide6.QtWidgets import QWidget

from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class WelcomeWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/WelcomeWidget.ui"

    def __init__(self):
        super(WelcomeWidget, self).__init__()
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
