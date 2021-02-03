from PySide6.QtWidgets import QWizardPage

from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class PasswordWizardPage(QWizardPage):
    UI_FILE = ROOT_DIR + "/ui/PasswordWizardPage.ui"

    def __init__(self, parent=None):
        super(PasswordWizardPage, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        # Connect signals/slots
        self.ui.passwordLineEdit.textChanged.connect(self.completeChanged)
        self.ui.confirmationLineEdit.textChanged.connect(self.completeChanged)

    def password(self) -> str:
        return self.ui.passwordLineEdit.text()

    def isComplete(self) -> bool:
        # TODO: REGEX
        return bool(
            self.ui.passwordLineEdit.text().strip() and
            self.ui.confirmationLineEdit.text().strip() and
            self.ui.passwordLineEdit.text() == self.confirmationLineEdit.text()
        )
