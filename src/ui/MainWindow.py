import logging
import sys
import webbrowser
from pathlib import Path

from typing import Optional

from PySide6 import QtCore
from PySide6.QtCore import Slot, QMetaObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QMenu, QApplication, QMessageBox

from src import ROOT_DIR
from src.db.DBConnection import DBConnection
from src.ui.dialog.AboutDialog import AboutDialog
from src.ui.dialog.ConfirmDeletionMessageBox import ConfirmDeletionMessageBox
from src.ui.dialog.DatabaseInformationDialog import DatabaseInformationDialog
from src.ui.widget.DatabaseWidget import DatabaseWidget
from src.ui.widget.EditEntryWidget import EditEntryWidget
from src.ui.widget.NewEntryWidget import NewEntryWidget
from src.ui.widget.PasswordGeneratorWidget import PasswordGeneratorWidget
from src.ui.widget.SearchBar import SearchBar
from src.ui.widget.UnlockDatabaseWidget import UnlockDatabaseWidget
from src.ui.widget.WelcomeWidget import WelcomeWidget
from src.ui import UiLoader
from src.util.Theme import is_dark_theme_enabled, icon_path


class MainWindow(QMainWindow):
    """
    Hauptfenster der Anwendung.
    """
    # UI-Datei
    UI_FILE = ROOT_DIR + "/ui/MainWindow.ui"

    # Icon-Datei
    ICON_FILE = ROOT_DIR + "/img/logo.svg"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues MainWindow-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(MainWindow, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        self.welcome_widget = WelcomeWidget(self)
        self.unlock_widget = UnlockDatabaseWidget(self)
        self.database_widget = DatabaseWidget(self)
        self.new_entry_widget = NewEntryWidget(self)
        self.edit_entry_widget = EditEntryWidget(self)
        self.password_generator_widget = PasswordGeneratorWidget(self)
        self.searchBar = SearchBar(self)

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.welcome_widget)
        self.stacked_widget.addWidget(self.unlock_widget)
        self.stacked_widget.addWidget(self.database_widget)
        self.stacked_widget.addWidget(self.new_entry_widget)
        self.stacked_widget.addWidget(self.edit_entry_widget)
        self.stacked_widget.addWidget(self.password_generator_widget)
        self.ui.toolBar.addWidget(self.searchBar)

        self.last_widget = None
        self.setCentralWidget(self.stacked_widget)
        self.setWindowIcon(QIcon(self.ICON_FILE))
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # Setup entryContextMenu
        self.entryContextMenu = QMenu(self)
        self.entryContextMenu.addAction(self.ui.actionNewEntry)
        self.entryContextMenu.addAction(self.ui.actionEditEntry)
        self.entryContextMenu.addAction(self.ui.actionDeleteEntry)
        self.entryContextMenu.addSeparator()
        self.entryContextMenu.addAction(self.ui.actionCopyUsername)
        self.entryContextMenu.addAction(self.ui.actionCopyPassword)
        self.entryContextMenu.addAction(self.ui.actionCopyUrl)
        self.entryContextMenu.addSeparator()
        self.entryContextMenu.addAction(self.ui.actionOpenUrl)

        # Connect signals / slots
        QMetaObject.connectSlotsByName(self)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.welcome_widget.open.connect(self.unlock_widget.on_database_changed)
        self.welcome_widget.open.connect(self.show_unlock_widget)
        self.unlock_widget.unlock.connect(self.database_widget.database_changed)
        self.unlock_widget.unlock.connect(self.show_database_widget)
        self.unlock_widget.cancel.connect(self.show_welcome_widget)
        self.database_widget.entrySelectionChanged.connect(self.edit_entry_widget.entry_changed)
        self.new_entry_widget.ok.connect(self.show_database_widget)
        self.new_entry_widget.cancel.connect(self.show_database_widget)
        self.new_entry_widget.entryCreated.connect(self.database_widget.new_entry)
        self.edit_entry_widget.ok.connect(self.show_database_widget)
        self.edit_entry_widget.cancel.connect(self.show_database_widget)
        self.edit_entry_widget.entryEdited.connect(self.database_widget.edit_entry)
        self.password_generator_widget.back.connect(self.show_last_widget)
        self.searchBar.textChanged.connect(self.database_widget.filter)

        self.set_action_icons()

    def set_action_icons(self) -> None:
        self.ui.actionOpenDatabase.setIcon(QIcon(str(icon_path / "document-open.svg")))
        self.ui.actionLockDatabase.setIcon(QIcon(str(icon_path / "object-locked.svg")))
        self.ui.actionNewEntry.setIcon(QIcon(str(icon_path / "entry-new.svg")))
        self.ui.actionEditEntry.setIcon(QIcon(str(icon_path / "entry-edit.svg")))
        self.ui.actionDeleteEntry.setIcon(QIcon(str(icon_path / "entry-delete.svg")))
        self.ui.actionCopyUsername.setIcon(QIcon(str(icon_path / "username-copy.svg")))
        self.ui.actionCopyPassword.setIcon(QIcon(str(icon_path / "password-copy.svg")))
        self.ui.actionCopyUrl.setIcon(QIcon(str(icon_path / "url-copy.svg")))
        self.ui.actionOpenUrl.setIcon(QIcon(str(icon_path / "web.svg")))
        self.ui.actionPasswordGenerator.setIcon(QIcon(str(icon_path / "password-generate.svg")))
        self.ui.actionAbout.setIcon(QIcon(str(icon_path / "help-about.svg")))

    @Slot()
    def on_actionNewDatabase_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für die Erstellung einer neuen Datenbank geklickt wurde.

        :return: None.
        """
        self.welcome_widget.create_new_database()

    @Slot()
    def on_actionOpenDatabase_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Öffnen einer Datenbank geklickt wurde.

        :return: None.
        """
        self.welcome_widget.open_database()

    @Slot()
    def on_actionCloseDatabase_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Schließen der Datenbank geklickt wurde.

        :return: None.
        """
        instance = DBConnection.instance()
        if instance is not None:
            instance.close()
        self.disable_database_actions()
        self.disable_entry_actions()
        self.show_welcome_widget()

    @Slot()
    def on_actionLockDatabase_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Sperren der Datenbank geklickt wurde.

        :return: None.
        """
        instance = DBConnection.instance()
        if instance is not None:
            instance.close()
        self.disable_database_actions()
        self.disable_entry_actions()
        self.show_unlock_widget()

    @Slot()
    def on_actionShowInformation_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Anzeigen der Datenbankinformationen geklickt wurde.

        :return: None.
        """
        DatabaseInformationDialog(self).exec_()

    @Slot()
    def on_actionExit_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Beenden der Anwendung geklickt wurde.

        :return: None.
        """
        instance = DBConnection.instance()
        if instance is not None:
            instance.close()
        sys.exit()

    @Slot()
    def on_actionNewEntry_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Erstellen eines neuen Eintrags geklickt wurde.

        :return: None.
        """
        self.show_new_entry_widget()

    @Slot()
    def on_actionEditEntry_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Bearbeiten eines Eintrags geklickt wurde.

        :return: None.
        """
        self.show_edit_entry_widget()

    @Slot()
    def on_actionDeleteEntry_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Löschen eines Eintrags geklickt wurde.

        :return: None.
        """
        message_box = ConfirmDeletionMessageBox(self)
        if message_box.exec_() == QMessageBox.Ok:
            self.database_widget.delete_selected_entry()

    @Slot()
    def on_actionCopyUsername_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Kopieren des Benutzernamens eines Eintrags geklickt wurde.

        :return: None.
        """
        clipboard = QApplication.clipboard()
        entry = self.database_widget.selected_entry()
        if entry and entry.username:
            clipboard.setText(entry.username)

    @Slot()
    def on_actionCopyPassword_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Kopieren des Passworts eines Eintrags geklickt wurde.

        :return: None.
        """
        clipboard = QApplication.clipboard()
        entry = self.database_widget.selected_entry()
        if entry and entry.password:
            clipboard.setText(entry.password)

    @Slot()
    def on_actionCopyUrl_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Kopieren der URL eines Eintrags geklickt wurde.

        :return: None.
        """
        clipboard = QApplication.clipboard()
        entry = self.database_widget.selected_entry()
        if entry and entry.url:
            clipboard.setText(entry.url)

    @Slot()
    def on_actionOpenUrl_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Öffnen der URL eines Eintrags geklickt wurde.

        :return: None.
        """
        entry = self.database_widget.selected_entry()
        if entry and entry.url:
            webbrowser.open(entry.url)

    @Slot()
    def on_actionPasswordGenerator_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Anzeigen des Passwortgenerators geklickt wurde.

        :return: None.
        """
        if self.ui.actionPasswordGenerator.isChecked():
            self.ui.actionOpenDatabase.setDisabled(True)
            self.last_widget = self.stacked_widget.currentWidget()
            self.show_password_generator_widget()
        else:
            self.show_last_widget()
            self.ui.actionOpenDatabase.setEnabled(True)

    @Slot()
    def on_actionAbout_triggered(self) -> None:
        """
        Wird aufgerufen, wenn die Aktion für das Anzeigen des Über-Dialogs geklickt wurde.

        :return: None.
        """
        AboutDialog(self).exec_()

    @Slot()
    def show_welcome_widget(self) -> None:
        """
        Zeigt das WelcomeWidget an.

        :return: None
        """
        self.stacked_widget.setCurrentWidget(self.welcome_widget)
        self.disable_entry_actions()

    @Slot()
    def show_unlock_widget(self) -> None:
        """
        Zeigt das UnlockWidget an.

        :return: None.
        """
        self.stacked_widget.setCurrentWidget(self.unlock_widget)
        self.disable_entry_actions()

    @Slot()
    def show_database_widget(self) -> None:
        """
        Zeigt das DatabaseWidget an.

        :return: None.
        """
        self.stacked_widget.setCurrentWidget(self.database_widget)
        self.enable_database_actions()
        self.enable_entry_actions()

    @Slot()
    def show_new_entry_widget(self) -> None:
        """
        Zeigt das NewEntryWidget an.

        :return: None.
        """
        self.stacked_widget.setCurrentWidget(self.new_entry_widget)
        self.disable_entry_actions()

    @Slot()
    def show_edit_entry_widget(self) -> None:
        self.stacked_widget.setCurrentWidget(self.edit_entry_widget)
        self.disable_entry_actions()

    @Slot()
    def show_password_generator_widget(self) -> None:
        self.stacked_widget.setCurrentWidget(self.password_generator_widget)
        self.disable_database_actions()
        self.disable_entry_actions()

    @Slot()
    def show_last_widget(self) -> None:
        self.ui.actionPasswordGenerator.setChecked(False)
        self.ui.actionOpenDatabase.setEnabled(True)
        if self.last_widget == self.welcome_widget:
            self.show_welcome_widget()
        elif self.last_widget == self.unlock_widget:
            self.show_unlock_widget()
        elif self.last_widget == self.database_widget:
            self.show_database_widget()
        elif self.last_widget == self.new_entry_widget:
            self.show_new_entry_widget()
        elif self.last_widget == self.edit_entry_widget:
            self.show_edit_entry_widget()

    @Slot()
    def showContextMenu(self, pos) -> None:
        """
        Zeigt das Kontextmenü an der übergebenen Position an.

        :param pos: Position.
        :return: None.
        """
        if self.stacked_widget.currentWidget() == self.database_widget:
            self.entryContextMenu.popup(self.sender().mapToGlobal(pos))

    def enable_database_actions(self) -> None:
        """
        Aktiviert die Datenbankaktionen.

        :return: None.
        """
        self.ui.actionCloseDatabase.setEnabled(True)
        self.ui.actionLockDatabase.setEnabled(True)
        self.ui.actionShowInformation.setEnabled(True)

    def disable_database_actions(self) -> None:
        """
        Deaktiviert die Datenbankaktionen.

        :return: None.
        """
        self.ui.actionCloseDatabase.setDisabled(True)
        self.ui.actionLockDatabase.setDisabled(True)
        self.ui.actionShowInformation.setDisabled(True)

    def enable_entry_actions(self) -> None:
        """
        Aktiviert die Eintrags-Aktionen.

        :return: None.
        """
        self.ui.actionNewEntry.setEnabled(True)
        self.searchBar.setEnabled(True)
        if self.database_widget.selected_entry():
            self.ui.actionEditEntry.setEnabled(True)
            self.ui.actionDeleteEntry.setEnabled(True)
            self.ui.actionCopyUsername.setEnabled(True)
            self.ui.actionCopyPassword.setEnabled(True)
            self.ui.actionCopyUrl.setEnabled(True)
            self.ui.actionOpenUrl.setEnabled(True)

    def disable_entry_actions(self) -> None:
        """
        Deaktiviert die Eintrags-Aktionen.

        :return: None.
        """
        self.ui.actionNewEntry.setDisabled(True)
        self.ui.actionEditEntry.setDisabled(True)
        self.ui.actionDeleteEntry.setDisabled(True)
        self.ui.actionCopyUsername.setDisabled(True)
        self.ui.actionCopyPassword.setDisabled(True)
        self.ui.actionCopyUrl.setDisabled(True)
        self.ui.actionOpenUrl.setDisabled(True)
        self.searchBar.setDisabled(True)
