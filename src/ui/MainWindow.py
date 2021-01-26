import sys

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow

from src.__main__ import ROOT_DIR
from src.ui.WelcomeWidget import WelcomeWidget
from src.ui import UiLoader


class MainWindow(QMainWindow):
    UI_FILE = ROOT_DIR + "/ui/MainWindow.ui"
    ICON_FILE = ROOT_DIR + "/img/logo.png"

    def __init__(self):
        super(MainWindow, self).__init__()

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.setWindowIcon(QIcon(self.ICON_FILE))
        self.setCentralWidget(WelcomeWidget())

        # Connect Signals / Slots
        self.ui.actionNewDatabase.triggered.connect(self.onNewDatabaseClicked)
        self.ui.actionOpenDatabase.triggered.connect(self.onOpenDatabaseClicked)
        self.ui.actionExit.triggered.connect(self.onExitClicked)


    @Slot()
    def onNewDatabaseClicked(self):
        print("New Database")

    @Slot()
    def onOpenDatabaseClicked(self):
        print("Open Database")

    @Slot()
    def onExitClicked(self):
        sys.exit(0)
