from PySide6.QtWidgets import QWidget

from src.__main__ import ROOT_DIR
from src.db.DatabaseConnection import DatabaseConnection
from src.ui import UiLoader


class DatabaseWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/DatabaseWidget.ui"

    def __init__(self, parent=None):
        super(DatabaseWidget, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self._connection = None

    @property
    def connection(self) -> DatabaseConnection:
        return self._connection

    @connection.setter
    def connection(self, connection: DatabaseConnection):
        self._connection = connection
