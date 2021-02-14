import logging
from typing import Optional

from PySide6.QtCore import Slot
from src.ui.widget.EntryWidget import EntryWidget


class EditEntryWidget(EntryWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(EditEntryWidget, self).__init__(parent)

        # Setup logging
        self.logger = logging.getLogger("Logger")

        # Setup UI
        self.ui.headerLabel.setText("Eintrag bearbeiten:")
        self.ui.okButton.setEnabled(False)

    @Slot()
    def on_okButton_clicked(self) -> None:
        self.ok.emit()

    @Slot()
    def on_cancelButton_clicked(self) -> None:
        self.cancel.emit()
