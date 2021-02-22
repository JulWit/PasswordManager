import logging
import sqlcipher3

from typing import Optional

from PySide6.QtCore import QMetaObject, Slot, Signal
from PySide6.QtWidgets import QWidget

from src.__main__ import ROOT_DIR
from src.db.DBConnection import DBConnection
from src.ui import UiLoader
from src.ui.dialog.DecryptionFailedMessageBox import DecryptionFailedMessageBox


class UnlockDatabaseWidget(QWidget):
    """
    Widget für das Entschlüsseln einer Datenbank.
    """

    # UI-Datei
    UI_FILE = ROOT_DIR + "/ui/UnlockDatabaseWidget.ui"

    # Signal, dass entsandt wird, wenn die Datenbank entschlüsselt werden soll
    unlock = Signal()

    # Signal, dass entsandt wird, wenn der abbrechen-Button geklickt wurde
    cancel = Signal()

    def __init__(self, parent: Optional[QWidget] = None, file: str = None) -> None:
        """
        Initialisiert ein neues UnlockDatabaseWidget-Objekt.

        :param parent: Übergeordnetes QWidget.
        :param file: Datenbankdatei.
        """
        super(UnlockDatabaseWidget, self).__init__(parent)

        # Datenbankdatei
        self._file = file

        # Setup logging
        self.logger = logging.getLogger("Logger")

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.ui.pathLabel.setText(file)
        self.ui.okButton.setEnabled(False)

        # Connect signals/slots
        QMetaObject.connectSlotsByName(self)
        self.ui.passwordLineEdit.textChanged.connect(self.password_changed)

    @Slot()
    def on_okButton_clicked(self) -> None:
        """
        Wird aufgerufen, wenn der ok-Button geklickt wurde.
        Versucht die Datenbank mit dem eigegebenen Passwort zu entschlüsseln.

        :return: None.
        """
        password = self.ui.passwordLineEdit.text()
        try:
            # DBConnection Singleton initialisieren
            instance = DBConnection.instance()
            if instance is not None:
                instance.close()
            DBConnection(self._file, password)
            self.unlock.emit()
            self.ui.passwordLineEdit.clear()
        except sqlcipher3.dbapi2.DatabaseError:
            DecryptionFailedMessageBox(self).exec_()

    @Slot()
    def on_cancelButton_clicked(self) -> None:
        """
        Wird aufgerufen, wenn der abbrechen-Button geklickt wurde. Entsendet ein cancel-Signal.

        :return: None.
        """
        self.cancel.emit()

    @Slot()
    def password_changed(self) -> None:
        """
        Wird aufgerufen, wenn das Passwort geändert wurde.
        Überprüft, ob das Passwort nichtleer ist und deaktiviert ggf. den ok-Button.

        :return: None.
        """
        password = bool(self.ui.passwordLineEdit.text().strip())
        self.ui.okButton.setEnabled(password)

    @Slot(str)
    def database_changed(self, file: str) -> None:
        """
        Wird aufgerufen, wenn die Datenbank gewechselt wurde.
        Setzt die aktuelle Datenbank.

        :param file: Datenbankdatei.
        :return: None
        """
        self.logger.debug(f"Datenbank: {file}")
        self._file = file
        self.ui.pathLabel.setText(file)
