import os

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow

from src.__main__ import ROOT_DIR
from src.ui.WelcomeWidget import WelcomeWidget
from src.ui import UiLoader


class MainWindow(QMainWindow):
    UI_FILE = "ui/MainWindow.ui"
    ICON_FILE = "img/logo.png"
    WINDOW_TITLE = "Passwort Manager"

    def __init__(self):
        super(MainWindow, self).__init__()
        uiFileDir = os.path.join(ROOT_DIR, self.UI_FILE)

        # Setup UI
        self.ui = UiLoader.loadUi(uiFileDir, self)
        self.setWindowIcon(QIcon(self.ICON_FILE))
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setCentralWidget(WelcomeWidget())

        # Connect Signals / Slots
        self.ui.actionNewDatabase.triggered.connect(self.onNewDatabaseClicked)
        self.ui.actionOpenDatabase.triggered.connect(self.onOpenDatabaseClicked)

    @Slot()
    def onNewDatabaseClicked(self):
        print("New Database")

    @Slot()
    def onOpenDatabaseClicked(self):
        print("Open Database")
