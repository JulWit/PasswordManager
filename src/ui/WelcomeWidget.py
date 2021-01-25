import os

from PySide6.QtWidgets import QWidget

from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class WelcomeWidget(QWidget):
    UI_FILE = "ui/WelcomeWidget.ui"

    def __init__(self):
        super(WelcomeWidget, self).__init__()
        uiFileDir = os.path.join(ROOT_DIR, self.UI_FILE)
        self.ui = UiLoader.loadUi(uiFileDir, self)
