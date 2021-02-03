import sqlcipher3
from PySide6.QtCore import QMetaObject, Slot, Signal
from PySide6.QtWidgets import QWidget

from src.__main__ import ROOT_DIR
from src.db.DatabaseConnection import DatabaseConnection
from src.ui import UiLoader
from src.ui.dialog.DecryptionFailedMessageBox import DecryptionFailedMessageBox


class UnlockDatabaseWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/UnlockDatabaseWidget.ui"

    unlock = Signal()
    cancel = Signal()

    def __init__(self, parent=None):
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
    def file(self, file: str):
        self._file = file
        self.ui.pathLabel.setText(file)

    @Slot()
    def on_okButton_clicked(self):
        password = self.ui.passwordLineEdit.text()
        try:
            connection = DatabaseConnection(self._file, password)
        except sqlcipher3.dbapi2.DatabaseError:
            DecryptionFailedMessageBox(self).exec_()

        self.unlock.emit()

    @Slot()
    def on_cancelButton_clicked(self):
        self.cancel.emit()

    @Slot()
    def password_changed(self):
        if self.ui.passwordLineEdit.text() == "":
            self.ui.okButton.setEnabled(False)
        else:
            self.ui.okButton.setEnabled(True)
