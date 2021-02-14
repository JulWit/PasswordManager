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
    cancel = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(UnlockDatabaseWidget, self).__init__(parent)
        self._file = None

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.ui.okButton.setEnabled(False)

        # Connect signals/slots
        QMetaObject.connectSlotsByName(self)
        self.ui.passwordLineEdit.textChanged.connect(self.password_changed)

    @property
    def file(self) -> str:
        return self._file

    @file.setter
    def file(self, file: str) -> None:
        self._file = file
        self.ui.pathLabel.setText(file)

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

