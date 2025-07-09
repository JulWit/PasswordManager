from typing import Optional

import sqlcipher3
from PySide6.QtCore import QMetaObject, Slot, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLineEdit

from src import ROOT_DIR
from src.db.DBConnection import DBConnection
from src.ui import UiLoader
from src.ui.dialog.DecryptionFailedMessageBox import DecryptionFailedMessageBox
from src.util.Theme import icon_path
from src.util.Logger import logger


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

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.ui.pathLabel.setText(file)
        self.ui.okButton.setEnabled(False)
        self.ui.echoButton.setIcon(QIcon(str(icon_path / "eye.svg")))

        # Connect signals/slots
        QMetaObject.connectSlotsByName(self)
        self.ui.passwordLineEdit.textChanged.connect(self.on_password_changed)

    @Slot()
    def on_okButton_clicked(self) -> None:
        """
        Wird aufgerufen, wenn der ok-Button geklickt wurde.
        Versucht die Datenbank mit dem eingegebenen Passwort zu entschlüsseln.

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
    def on_echoButton_clicked(self) -> None:
        """
        Wird aufgerufen, wenn der Password-Anzeigen-Button geklickt wurde.
        Zeigt das Passwort an oder versteckt es wieder.

        :return: None.
        """
        lineEdit = self.ui.passwordLineEdit
        if lineEdit.echoMode() == QLineEdit.EchoMode.Password:
            lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.echoButton.setIcon(QIcon(str(icon_path / "eye-off.svg")))
        else:
            lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.echoButton.setIcon(QIcon(str(icon_path / "eye.svg")))

    @Slot()
    def on_cancelButton_clicked(self) -> None:
        """
        Wird aufgerufen, wenn der abbrechen-Button geklickt wurde. Entsendet ein cancel-Signal.

        :return: None.
        """
        self.ui.passwordLineEdit.clear()
        self.cancel.emit()

    @Slot()
    def on_password_changed(self) -> None:
        """
        Wird aufgerufen, wenn das Passwort geändert wurde.
        Überprüft, ob das Passwort nichtleer ist und deaktiviert ggf. den ok-Button.

        :return: None.
        """
        password = bool(self.ui.passwordLineEdit.text().strip())
        self.ui.okButton.setEnabled(password)



    @Slot(str)
    def on_database_changed(self, file: str) -> None:
        """
        Wird aufgerufen, wenn die Datenbank gewechselt wurde.
        Setzt die aktuelle Datenbank.

        :param file: Datenbankdatei.
        :return: None
        """
        logger.debug(f"Datenbank: {file}")
        self._file = file
        self.ui.pathLabel.setText(file)


