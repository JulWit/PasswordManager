from PySide6.QtCore import Signal, Slot, QMetaObject
from PySide6.QtWidgets import QWidget, QLineEdit
from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class EntryWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/EntryWidget.ui"

    cancel = Signal()
    ok = Signal()

    def __init__(self, parent=None) -> None:
        super(EntryWidget, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        # Connect signals/slots
        QMetaObject.connectSlotsByName(self)
        self.ui.titleLineEdit.textChanged.connect(self.entry_information_changed)

    @Slot()
    def on_okButton_clicked(self) -> None:
        raise NotImplementedError("Die Methode on_okButton_clicked muss durch "
                                  "abgeleitete Klassen überschrieben werden")

    @Slot()
    def on_cancelButton_clicked(self) -> None:
        raise NotImplementedError("Die Methode on_cancelButton_clicked muss durch "
                                  "abgeleitete Klassen überschrieben werden")

    @Slot()
    def entry_information_changed(self) -> None:
        title = bool(self.ui.titleLineEdit.text().strip())
        self.ui.okButton.setEnabled(title)

    def clear(self) -> None:
        line_edits = self.ui.findChildren(QLineEdit)
        for line_edit in line_edits:
            line_edit.clear()
        self.ui.notesTextEdit.clear()
