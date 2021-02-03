from PySide6.QtCore import QMetaObject, Slot, Signal
from PySide6.QtWidgets import QWidget, QMessageBox

from src.__main__ import ROOT_DIR
from src.db.DBConnection import DBConnection
from src.ui import UiLoader


class UnlockDatabaseWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/UnlockDatabaseWidget.ui"

    def __init__(self, parent, file):
        super(UnlockDatabaseWidget, self).__init__(parent)
        self._file = file

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.ui.pathLabel.setText(file)

        # Signals
        self.unlock = Signal()
        self.cancel = Signal()

        # Connect signals/slots
        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_okButton_clicked(self):
        password = self.ui.passwordLineEdit.text()
        try:
            connection = DBConnection(self._file, password)
        except ValueError:
            error_message = QMessageBox()
            error_message.setWindowTitle("Entschlüsselung fehlgeschlagen")
            error_message.setText("Die Datenbank konnte nicht entschlüsselt werden")
            error_message.setInformativeText("Das eingegebene Passwort ist falsch.")

    @Slot()
    def on_cancelButton_clicked(self):
        self.cancel.emit()
