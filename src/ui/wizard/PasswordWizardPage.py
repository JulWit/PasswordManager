from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWizardPage, QWidget

from src.__main__ import ROOT_DIR
from src.ui import UiLoader
from src.util import PasswordUtils


class PasswordWizardPage(QWizardPage):
    UI_FILE = ROOT_DIR + "/ui/PasswordWizardPage.ui"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
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
    def passwordLineEdit_changed(self) -> None:
        strength = PasswordUtils.evaluate_password_strength(self.password())
        color = "white"
        if 0 <= strength < 0.25:
            color = "red"
        if 0.25 < strength < 0.50:
            color = "orange"
        elif 0.50 < strength < 0.75:
            color = "MediumSeaGreen"
        elif 0.75 < strength <= 1:
            color = "green"
        self.ui.passwordStrength.setStyleSheet("QProgressBar::chunk{background-color: " + color + "}")
        self.ui.passwordStrength.setValue(round(strength * 100, 0))

    def isComplete(self) -> bool:
        return bool(self.ui.passwordLineEdit.text().strip() and
                    self.ui.confirmationLineEdit.text().strip() and
                    self.ui.passwordLineEdit.text() == self.confirmationLineEdit.text())
