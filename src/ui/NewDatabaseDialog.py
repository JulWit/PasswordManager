from PySide6.QtWidgets import QWizard

from src.ui import UiLoader


class NewDatabaseDialog(QWizard):
    UI_FILE = "../../ui/NewDatabaseWizard.ui"

    def __init__(self):
        super(NewDatabaseDialog, self).__init__()

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
