import logging
import sqlcipher3

from PySide6.QtCore import QDir, QMetaObject, Slot, Signal
from PySide6.QtWidgets import QWidget, QFileDialog

from src.__main__ import ROOT_DIR
from src.ui import UiLoader
from src.ui.dialog.DatabaseCreationFailedMessageBox import DatabaseCreationFailedMessageBox
from src.ui.wizard.NewDatabaseWizard import NewDatabaseWizard


class WelcomeWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/WelcomeWidget.ui"

    open = Signal(str)

    def __init__(self, parent) -> None:
        super(WelcomeWidget, self).__init__(parent)

        # Setup logging
        self.logger = logging.getLogger('Logger')

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        # Connect signals / slots
        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_newDatabaseButton_clicked(self) -> None:
        self.create_new_database()

    @Slot()
    def on_openDatabaseButton_clicked(self) -> None:
        self.open_database()

    def create_new_database(self) -> None:
        # Neuen Wizard erstellen und anzeigen
        wizard = NewDatabaseWizard(self)
        if wizard.exec_():
            # Datenbankinformationen auslesen
            data = wizard.database_data()

            # Speicherort der Datenbank erfragen
            file = QFileDialog.getSaveFileName(self,
                                               "Datenbank speichern",
                                               QDir.homePath() + f"/{data.name}.db")[0]

            # Wenn das Speichern abgebrochen wurde ist file = None
            if file:
                connection = None
                try:
                    connection = sqlcipher3.connect(file)
                    cursor = connection.cursor()
                    cursor.execute(f"PRAGMA KEY={data.password}")
                    cursor.execute("""CREATE TABLE Entries (
                                            id          INTEGER PRIMARY KEY AUTOINCREMENT,
                                            title       VARCHAR(128) NOT NULL,
                                            username    VARCHAR(128) NOT NULL,
                                            password    VARCHAR(128) NOT NULL,
                                            url         VARCHAR(1024),
                                            notes       VARCHAR(128),
                                            date        DATE DEFAULT CURRENT_TIMESTAMP
                                        );"""
                                   )
                    connection.commit()
                except sqlcipher3.dbapi2.DatabaseError as e:
                    connection.close()
                    self.logger.error(f"Datenbank: {file} konnte nicht erstellt werden: {e}")
                    DatabaseCreationFailedMessageBox(self).exec_()

                self.logger.debug(f"Datenbank: {file} erfolgreich erstellt")
            else:
                self.logger.debug("Speicherung der Datenbank abgebrochen")

    def open_database(self) -> None:
        file = QFileDialog.getOpenFileName(self,
                                           "Datenbank öffnen",
                                           QDir.homePath(),
                                           "Datenbank Dateien (*.db)")[0]
        if file:
            self.open.emit(file)
