from typing import Optional

from PySide6.QtWidgets import QMessageBox, QWidget


class ConfirmDeletionMessageBox(QMessageBox):
    """
    MessageBox, die den Benutzer fragt, ob er das ausgewählte Element wirklich löschen möchte.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues ConfirmDeletionMessageBox-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(ConfirmDeletionMessageBox, self).__init__(parent)
        self.setWindowTitle("Eintrag löschen")
        self.setText("Möchten sie den ausgewählten Eintrag wirklich löschen?")
        self.setIcon(QMessageBox.Icon.Question)
        self.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
