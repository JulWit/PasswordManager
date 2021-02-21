from typing import Optional

from PySide6.QtWidgets import QMessageBox, QWidget


class ConfirmDeletetionMessageBox(QMessageBox):
    """
    MessageBox, die den Benutzer fragt, ob er das ausgewählte Element wirklich löschen möchte.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiet ein neues ConfirmDeletetionMessageBox-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(ConfirmDeletetionMessageBox, self).__init__(parent)
        self.setWindowTitle("Eintrag löschen")
        self.setText("Möchten sie den ausgewählten Eintrag wirklich löschen?")
        self.setIcon(QMessageBox.Question)
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
