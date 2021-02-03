import logging
import sys
import sqlcipher3

from PySide6.QtCore import Slot, QMetaObject, QDir
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QFileDialog, QStackedWidget

from src.__main__ import ROOT_DIR
from src.ui.dialog.DatabaseCreationFailedMessageBox import DatabaseCreationFailedMessageBox
from src.ui.widget.UnlockDatabaseWidget import UnlockDatabaseWidget
from src.ui.widget.WelcomeWidget import WelcomeWidget
from src.ui.wizard.NewDatabaseWizard import NewDatabaseWizard
from src.ui import UiLoader


class MainWindow(QMainWindow):
    UI_FILE = ROOT_DIR + "/ui/MainWindow.ui"
    ICON_FILE = ROOT_DIR + "/img/logo.png"

    def __init__(self):
        super(MainWindow, self).__init__()

        # Setup logging
        self.logger = logging.getLogger('Logger')

        # Setup database
        self.db_connection = None

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.welcome_widget = WelcomeWidget(self)
        self.unlock_widget = UnlockDatabaseWidget(self)
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.welcome_widget)
        self.stacked_widget.addWidget(self.unlock_widget)
        self.setCentralWidget(self.stacked_widget)
        self.setWindowIcon(QIcon(self.ICON_FILE))

        # Connect signals / slots
        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_actionNewDatabase_triggered(self):
        self.welcome_widget.create_new_database()

    @Slot()
    def on_actionOpenDatabase_triggered(self):
        self.welcome_widget.open_database()

    @Slot()
    def on_actionExit_triggered(self):
        sys.exit()
