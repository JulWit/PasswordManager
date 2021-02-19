import re
from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWizardPage, QWidget

from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class NameWizardPage(QWizardPage):
    UI_FILE = ROOT_DIR + "/ui/NameWizardPage.ui"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(NameWizardPage, self).__init__(parent)

        # Setup Pattern
        self.pattern = re.compile(r"^[^\s]{1,128}$")

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        # Connect signals/slots
        self.ui.nameLineEdit.textChanged.connect(self.completeChanged)

    def name(self) -> str:
        return self.ui.nameLineEdit.text()

    def description(self) -> str:
        return self.descriptionLineEdit.text()

    @Slot()
    def isComplete(self) -> bool:
        return bool(self.pattern.match(self.ui.nameLineEdit.text()))


