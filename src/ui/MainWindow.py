import logging
import sys

from PySide6.QtCore import Slot, QMetaObject, QDir
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QFileDialog

from src.__main__ import ROOT_DIR
from src.db.DBConnection import DBConnection
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

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.central_widget = WelcomeWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setWindowIcon(QIcon(self.ICON_FILE))

        # Setup database
        self.db_connection = None

        # Connect signals / slots
        QMetaObject.connectSlotsByName(self)
        QMetaObject.connectSlotsByName(self.central_widget)

    @Slot()
    def on_actionNewDatabase_triggered(self):
        self.create_new_database()

    @Slot()
    def on_actionOpenDatabase_triggered(self):
        self.open_database()

    @Slot()
    def on_actionExit_triggered(self):
        sys.exit()

    @Slot()
    def on_newDatabaseButton_clicked(self):
        self.create_new_database()

    @Slot()
    def on_openDatabaseButton_clicked(self):
        self.open_database()

    def create_new_database(self):
        # Neuen Wizard erstellen und anzeigen
        wizard = NewDatabaseWizard(self)
        if wizard.exec_():
            # Datenbankinformationen auslesen
            data = wizard.database_data()

            # Speicherort der Datenbank erfragen
            file = QFileDialog.getSaveFileName(self,
                                               self.tr("Datenbank speichern"),
                                               QDir.homePath() + f"/{data.name}.db")[0]

            # Wenn das Speichern abgebrochen wurde ist file = None
            if file:
                # Datenbank erstellen und Verbindung aufbauen
                self.db_connection = DBConnection(file, data.password)
            else:
                self.logger.debug("Speicherung der Datenbank abgebrochen")

    def open_database(self):
        file = QFileDialog.getOpenFileName(self,
                                           self.tr("Datenbank öffnen"),
                                           QDir.homePath(),
                                           self.tr("Datenbank Dateien (*.db)"))[0]
        if file:
            self.logger.debug(f"Datenbank: {file} geöffnet")
            self.setCentralWidget(UnlockDatabaseWidget(self, file))
