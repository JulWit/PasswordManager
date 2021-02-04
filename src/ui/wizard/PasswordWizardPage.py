from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWizardPage

from src.__main__ import ROOT_DIR
from src.ui import UiLoader
from src.util import PasswordUtils


class PasswordWizardPage(QWizardPage):
    UI_FILE = ROOT_DIR + "/ui/PasswordWizardPage.ui"

    def __init__(self, parent=None):
        super(PasswordWizardPage, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        # Connect signals/slots
        self.ui.passwordLineEdit.textChanged.connect(self.passwordLineEdit_changed)
        self.ui.passwordLineEdit.textChanged.connect(self.completeChanged)
        self.ui.confirmationLineEdit.textChanged.connect(self.completeChanged)

    def password(self) -> str:
        return self.ui.passwordLineEdit.text()

    # Beurteilung der Passwortstärke
    def passwordLineEdit_changed(self):
        strength = PasswordUtils.evaluate_password(self.password())
        self.ui.passwordStrength.setStyleSheet("QProgressBar::chunk{background-color: red}")
        self.ui.passwordStrength.setValue(strength * 100)

    def isComplete(self) -> bool:
        # TODO: REGEX
        return bool(
            self.ui.passwordLineEdit.text().strip() and
            self.ui.confirmationLineEdit.text().strip() and
            self.ui.passwordLineEdit.text() == self.confirmationLineEdit.text()
        )
