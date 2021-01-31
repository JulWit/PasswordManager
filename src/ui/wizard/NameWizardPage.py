from PySide6.QtWidgets import QWizardPage

from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class NameWizardPage(QWizardPage):
    UI_FILE = ROOT_DIR + "/ui/NameWizardPage.ui"

    def __init__(self, parent):
        super(NameWizardPage, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        # Connect signal/slots
        self.ui.nameLineEdit.textChanged.connect(self.completeChanged)

    def name(self) -> str:
        return self.ui.nameLineEdit.text()

    def description(self) -> str:
        return self.descriptionLineEdit.text()

    def isComplete(self) -> bool:
        # TODO: REGEX
        return bool(self.ui.nameLineEdit.text().strip())
