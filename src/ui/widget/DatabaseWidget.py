import logging

from PySide6.QtCore import Slot
from PySide6.QtGui import QShowEvent, Qt
from PySide6.QtWidgets import QWidget, QHeaderView

from src.__main__ import ROOT_DIR
from src.db.DBConnection import DBConnection
from src.db.TableModel import TableModel
from src.ui import UiLoader


class DatabaseWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/DatabaseWidget.ui"

    def __init__(self, parent=None):
        super(DatabaseWidget, self).__init__(parent)

        # Setup logging
        self.logger = logging.getLogger("Logger")

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.ui.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.ui.tableView.setSortingEnabled(True)
        self.ui.tableView.resizeColumnsToContents()

    def set_layout(self):
        """ Layout der TableView anpassen """

        # ID- und Passwort-Spalte ausblenden
        self.ui.tableView.setColumnHidden(0, True)
        self.ui.tableView.setColumnHidden(3, True)

        # Erste Zeile auswählen
        self.ui.tableView.selectRow(0)

    def showEvent(self, event: QShowEvent) -> None:
        entry_list = DBConnection().query("SELECT * FROM Entries")
        entry_model = TableModel(entry_list)

        self.ui.tableView.setModel(entry_model)
        self.set_layout()

    @Slot()
    def delete_entry(self):
        selection_model = self.ui.tableView.selectionModel()
        if selection_model.hasSelection():
            model = self.ui.tableView.model()
            index = selection_model.currentIndex()
            entry_id = index.sibling(index.row(), 0).data()

            query = f"DELETE FROM Entries WHERE id = {entry_id}"
            connection = DBConnection()
            connection.execute(query)
            connection.commit()

            removed = model.removeRow(index.row())
            self.logger.debug(f"Eintrag {entry_id} entfernt: {removed}")

