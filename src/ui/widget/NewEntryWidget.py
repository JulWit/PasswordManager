from PySide6.QtCore import Slot, Signal, QMetaObject
from PySide6.QtWidgets import QWidget

from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class NewEntryWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/NewEntryWidget.ui"

    cancel = Signal()
    ok = Signal()

    def __init__(self, parent=None):
        super(NewEntryWidget, self).__init__(parent)

        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        # Connect signals/slots
        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_okButton_clicked(self):
        self.ok.emit()

    @Slot()
    def on_cancelButton_clicked(self):
        self.cancel.emit()
