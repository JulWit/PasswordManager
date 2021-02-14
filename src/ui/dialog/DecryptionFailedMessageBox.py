from typing import Optional

from PySide6.QtWidgets import QMessageBox, QWidget


class DecryptionFailedMessageBox(QMessageBox):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(DecryptionFailedMessageBox, self).__init__(parent)

        self.setWindowTitle("Entschlüsselung fehlgeschlagen")
        self.setIcon(QMessageBox.Critical)
        self.setText("Die Datenbank konnte nicht entschlüsselt werden")
        self.setInformativeText("Das eingegebene Passwort ist falsch.")
