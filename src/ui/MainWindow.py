import logging
import sys

from PySide6.QtCore import Slot, QMetaObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from src.__main__ import ROOT_DIR
from src.ui.widget.DatabaseWidget import DatabaseWidget
from src.ui.widget.NewEntryWidget import NewEntryWidget
from src.ui.widget.UnlockDatabaseWidget import UnlockDatabaseWidget
from src.ui.widget.WelcomeWidget import WelcomeWidget
from src.ui import UiLoader


class MainWindow(QMainWindow):
    UI_FILE = ROOT_DIR + "/ui/MainWindow.ui"
    ICON_FILE = ROOT_DIR + "/img/logo.svg"

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Setup logging
        self.logger = logging.getLogger('Logger')

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.welcome_widget = WelcomeWidget(self)
        self.unlock_widget = UnlockDatabaseWidget(self)
        self.database_widget = DatabaseWidget(self)
        self.new_entry_widget = NewEntryWidget(self)

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.welcome_widget)
        self.stacked_widget.addWidget(self.unlock_widget)
        self.stacked_widget.addWidget(self.database_widget)
        self.stacked_widget.addWidget(self.new_entry_widget)

        self.setCentralWidget(self.stacked_widget)
        self.setWindowIcon(QIcon(self.ICON_FILE))

        # Connect signals / slots
        QMetaObject.connectSlotsByName(self)
        self.welcome_widget.open.connect(self.show_unlock_widget)
        self.unlock_widget.cancel.connect(self.show_welcome_widget)
        self.unlock_widget.unlock.connect(self.show_database_widget)
        self.new_entry_widget.ok.connect(self.show_database_widget)
        self.new_entry_widget.cancel.connect(self.show_database_widget)

        self.ui.actionDeleteEntry.triggered.connect(self.database_widget.delete_entry)

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
    def on_actionNewEntry_triggered(self):
        self.stacked_widget.setCurrentWidget(self.new_entry_widget)

    @Slot()
    def on_actionEditEntry_triggered(self):
        pass

    @Slot()
    def show_welcome_widget(self):
        self.stacked_widget.setCurrentWidget(self.welcome_widget)
        self.change_actions_enabled(False)

    @Slot(str)
    def show_unlock_widget(self, file: str):
        self.unlock_widget.file = file
        self.stacked_widget.setCurrentWidget(self.unlock_widget)
        self.change_actions_enabled(False)

    @Slot()
    def show_database_widget(self):
        self.stacked_widget.setCurrentWidget(self.database_widget)
        self.change_actions_enabled(True)

    def change_actions_enabled(self, enabled=False):
        self.ui.actionNewEntry.setEnabled(enabled)
        self.ui.actionEditEntry.setEnabled(enabled)
        self.ui.actionDeleteEntry.setEnabled(enabled)
