import logging
from typing import Optional

import sqlcipher3

from PySide6.QtCore import QMetaObject, Slot, Signal
from PySide6.QtWidgets import QWidget

from src.__main__ import ROOT_DIR
from src.db.DBConnection import DBConnection
from src.ui import UiLoader
from src.ui.dialog.DecryptionFailedMessageBox import DecryptionFailedMessageBox


class UnlockDatabaseWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/UnlockDatabaseWidget.ui"

    unlock = Signal()
    # ok = Signal()
    cancel = Signal()

    def __init__(self, parent: Optional[QWidget] = None, file: str = None) -> None:
        super(UnlockDatabaseWidget, self).__init__(parent)
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
        self.cancel.emit()

    @Slot()
    def password_changed(self) -> None:
        password = bool(self.ui.passwordLineEdit.text().strip())
        self.ui.okButton.setEnabled(password)

    @Slot(str)
    def set_database(self, file: str):
        self.logger.debug(f"Datenbank: {file}")
        self._file = file
        self.ui.pathLabel.setText(file)
