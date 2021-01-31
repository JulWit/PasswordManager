from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWizard

from src.__main__ import ROOT_DIR
from src.db.DatabaseData import DatabaseData
from src.ui import UiLoader
from src.ui.wizard.NameWizardPage import NameWizardPage
from src.ui.wizard.PasswordWizardPage import PasswordWizardPage


class NewDatabaseWizard(QWizard):
    UI_FILE = ROOT_DIR + "/ui/NewDatabaseWizard.ui"
    BACKGROUND_IMAGE = ROOT_DIR + "/img/logo.png"

    def __init__(self, parent):
        super(NewDatabaseWizard, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.setPixmap(self.BackgroundPixmap, QPixmap(self.BACKGROUND_IMAGE))

        # Add pages
        self.name_page = NameWizardPage(self)
        self.password_page = PasswordWizardPage(self)
        self.addPage(self.name_page)
        self.addPage(self.password_page)

    def get_database_data(self) -> DatabaseData:
        name = self.name_page.name()
        description = self.name_page.description()
        password = self.password_page.password()
        return DatabaseData(name, password, description)
