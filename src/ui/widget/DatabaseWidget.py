from PySide6.QtGui import QShowEvent, Qt
from PySide6.QtWidgets import QWidget, QHeaderView

from src.__main__ import ROOT_DIR
from src.db.DatabaseConnection import DBConnection
from src.db.TableModel import TableModel
from src.ui import UiLoader


class DatabaseWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/DatabaseWidget.ui"

    def __init__(self, parent=None):
        super(DatabaseWidget, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

    def set_layout(self):
        """ Layout der TableView anpassen """
        # ID Spalte ausblenden
        self.ui.tableView.setColumnHidden(0, True)
        # Erste Zeile auswählen
        self.ui.tableView.selectRow(0)

    def showEvent(self, event: QShowEvent) -> None:
        entry_list = DBConnection().query('SELECT * FROM Entries')
        # print(entry_list)
        entry_model = TableModel(entry_list)
        self.ui.tableView.setModel(entry_model)
        self.set_layout()
