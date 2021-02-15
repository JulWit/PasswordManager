import logging
import sys
from typing import Optional

from PySide6.QtCore import Slot, QMetaObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget

from src.__main__ import ROOT_DIR
from src.db.DBConnection import DBConnection
from src.db.Entry import Entry
from src.ui.widget.DatabaseWidget import DatabaseWidget
from src.ui.widget.EditEntryWidget import EditEntryWidget
from src.ui.widget.NewEntryWidget import NewEntryWidget
from src.ui.widget.UnlockDatabaseWidget import UnlockDatabaseWidget
from src.ui.widget.WelcomeWidget import WelcomeWidget
from src.ui import UiLoader


class MainWindow(QMainWindow):
    UI_FILE = ROOT_DIR + "/ui/MainWindow.ui"
    ICON_FILE = ROOT_DIR + "/img/logo.svg"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(MainWindow, self).__init__(parent)

        # Setup logging
        self.logger = logging.getLogger('Logger')

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.welcome_widget = WelcomeWidget(self)
        self.unlock_widget = None
        self.database_widget = None
        self.new_entry_widget = None
        self.edit_entry_widget = None

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.welcome_widget)
        self.setCentralWidget(self.stacked_widget)
        self.setWindowIcon(QIcon(self.ICON_FILE))

        # Connect signals / slots
        QMetaObject.connectSlotsByName(self)
        self.welcome_widget.open.connect(self.show_unlock_widget)

    @Slot()
    def on_actionNewDatabase_triggered(self) -> None:
        self.welcome_widget.create_new_database()

    @Slot()
    def on_actionOpenDatabase_triggered(self) -> None:
        self.welcome_widget.open_database()

    @Slot()
    def on_actionExit_triggered(self) -> None:
        instance = DBConnection.instance()
        if instance is not None:
            instance.close()
        sys.exit()

    @Slot()
    def on_actionNewEntry_triggered(self) -> None:
        self.show_new_entry_widget()

    @Slot()
    def on_actionEditEntry_triggered(self) -> None:
        model = self.database_widget.model
        selection_model = self.database_widget.selection_model
        if selection_model.hasSelection():
            index = selection_model.currentIndex()
            entry = model.entries[index.row()]
            self.show_edit_entry_widget(entry)

    @Slot()
    def on_actionDeleteEntry_triggered(self) -> None:
        selection_model = self.database_widget.selection_model
        if selection_model.hasSelection():
            index = selection_model.currentIndex()
            self.database_widget.delete_entry(index)

    @Slot()
    def show_welcome_widget(self) -> None:
        self.stacked_widget.setCurrentWidget(self.welcome_widget)
        self.disable_entry_actions()

    @Slot(str)
    def show_unlock_widget(self, file: str) -> None:
        if self.unlock_widget is None:
            self.create_unlock_widget(file)
        self.stacked_widget.setCurrentWidget(self.unlock_widget)
        self.disable_entry_actions()

    @Slot()
    def show_database_widget(self) -> None:
        if self.database_widget is None:
            self.create_database_widget()
        self.stacked_widget.setCurrentWidget(self.database_widget)
        self.enable_entry_actions()

    @Slot()
    def show_new_entry_widget(self) -> None:
        if self.new_entry_widget is None:
            self.create_new_entry_widget()
        self.stacked_widget.setCurrentWidget(self.new_entry_widget)
        self.disable_entry_actions()

    @Slot()
    def show_edit_entry_widget(self, entry_id) -> None:
        self.create_edit_entry_widget(entry_id)
        self.stacked_widget.setCurrentWidget(self.edit_entry_widget)
        self.disable_entry_actions()

    def create_unlock_widget(self, file: str) -> None:
        self.unlock_widget = UnlockDatabaseWidget(file, self)
        self.unlock_widget.cancel.connect(self.show_welcome_widget)
        self.unlock_widget.unlock.connect(self.show_database_widget)
        self.stacked_widget.addWidget(self.unlock_widget)

    def create_database_widget(self) -> None:
        self.database_widget = DatabaseWidget(self)
        self.stacked_widget.addWidget(self.database_widget)

    def create_new_entry_widget(self) -> None:
        self.new_entry_widget = NewEntryWidget(self)
        self.new_entry_widget.ok.connect(self.show_database_widget)
        self.new_entry_widget.cancel.connect(self.show_database_widget)
        self.new_entry_widget.newEntryCreated.connect(self.database_widget.new_entry)
        self.stacked_widget.addWidget(self.new_entry_widget)

    def create_edit_entry_widget(self, entry: Entry) -> None:
        self.edit_entry_widget = EditEntryWidget(entry, self)
        self.edit_entry_widget.ok.connect(self.show_database_widget)
        self.edit_entry_widget.cancel.connect(self.show_database_widget)
        self.edit_entry_widget.edited.connect(self.database_widget.edit_entry)
        self.stacked_widget.addWidget(self.edit_entry_widget)

    def enable_entry_actions(self) -> None:
        self.ui.actionNewEntry.setEnabled(True)
        self.ui.actionEditEntry.setEnabled(True)
        self.ui.actionDeleteEntry.setEnabled(True)

    def disable_entry_actions(self) -> None:
        self.ui.actionNewEntry.setDisabled(True)
        self.ui.actionEditEntry.setDisabled(True)
        self.ui.actionDeleteEntry.setDisabled(True)
