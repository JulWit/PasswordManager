from PySide6.QtWidgets import QMessageBox


class ConfirmDeletetionMessageBox(QMessageBox):
    def __init__(self, parent=None) -> None:
        super(ConfirmDeletetionMessageBox, self).__init__(parent)

        self.setWindowTitle("Eintrag löschen")
        self.setText("Möchten sie den ausgewählten Eintrag wirklich löschen?")
