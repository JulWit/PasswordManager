from typing import Optional

from PySide6.QtWidgets import QMessageBox, QWidget


class DecryptionFailedMessageBox(QMessageBox):
    """
    MessageBox, die den Benutzer darüber informiert, dass die Verschlüsselung fehlgeschlagen ist.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues DecryptionFailedMessageBox-Objekt.
        :param parent: Übergeordnetes QWidget.
        """
        super(DecryptionFailedMessageBox, self).__init__(parent)
        self.setWindowTitle("Entschlüsselung fehlgeschlagen")
        self.setText("Die Datenbank konnte nicht entschlüsselt werden")
        self.setInformativeText("Das eingegebene Passwort ist falsch.")
        self.setIcon(QMessageBox.Icon.Critical)
