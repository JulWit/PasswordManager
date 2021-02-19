from typing import Optional

from PySide6.QtWidgets import QMessageBox, QWidget


class ConfirmDeletetionMessageBox(QMessageBox):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(ConfirmDeletetionMessageBox, self).__init__(parent)

        self.setWindowTitle("Eintrag löschen")
        self.setText("Möchten sie den ausgewählten Eintrag wirklich löschen?")
        self.setIcon(QMessageBox.Question)
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

