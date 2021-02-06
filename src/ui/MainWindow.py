import logging
import sys

from PySide6.QtCore import Slot, QMetaObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from src.__main__ import ROOT_DIR
from src.db.DatabaseConnection import DatabaseConnection
from src.ui.widget.DatabaseWidget import DatabaseWidget
from src.ui.widget.UnlockDatabaseWidget import UnlockDatabaseWidget
from src.ui.widget.WelcomeWidget import WelcomeWidget
from src.ui import UiLoader


class MainWindow(QMainWindow):
    UI_FILE = ROOT_DIR + "/ui/MainWindow.ui"
    ICON_FILE = ROOT_DIR + "/img/logo.png"

    def __init__(self):
        super(MainWindow, self).__init__()

        # Setup logging
        self.logger = logging.getLogger('Logger')

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.welcome_widget = WelcomeWidget(self)
        self.unlock_widget = UnlockDatabaseWidget(self)
        self.database_widget = DatabaseWidget(self)

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.welcome_widget)
        self.stacked_widget.addWidget(self.unlock_widget)
        self.stacked_widget.addWidget(self.database_widget)

        self.setCentralWidget(self.stacked_widget)
        self.setWindowIcon(QIcon(self.ICON_FILE))

        # Connect signals / slots
        QMetaObject.connectSlotsByName(self)
        self.welcome_widget.open.connect(self.show_unlock_widget)
        self.unlock_widget.cancel.connect(self.show_welcome_widget)
        self.unlock_widget.unlock.connect(self.show_database_widget)

    @Slot()
    def on_actionNewDatabase_triggered(self):
        self.welcome_widget.create_new_database()

    @Slot()
    def on_actionOpenDatabase_triggered(self):
        self.welcome_widget.open_database()

    @Slot()
    def on_actionExit_triggered(self):
        sys.exit()

    @Slot()
    def show_welcome_widget(self):
        self.stacked_widget.setCurrentWidget(self.welcome_widget)
        self.change_actions_enabled(False)

    @Slot(str)
    def show_unlock_widget(self, file: str):
        self.unlock_widget.file = file
        self.stacked_widget.setCurrentWidget(self.unlock_widget)
        self.change_actions_enabled(False)

    @Slot(DatabaseConnection)
    def show_database_widget(self, connection: DatabaseConnection):
        self.database_widget.connection = connection
        self.stacked_widget.setCurrentWidget(self.database_widget)
        self.change_actions_enabled(True)

    def change_actions_enabled(self, enabled=False):
        self.ui.actionNewEntry.setEnabled(enabled)
        self.ui.actionEditEntry.setEnabled(enabled)
        self.ui.actionDeleteEntry.setEnabled(enabled)

