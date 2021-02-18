import logging
from typing import Optional

from PySide6 import QtCore
from PySide6.QtCore import Slot, Signal, QModelIndex
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget

from src.__main__ import ROOT_DIR
from src.db.DBConnection import DBConnection
from src.db.Entry import Entry
from src.db.TableModel import TableModel
from src.ui import UiLoader
from src.ui.widget.EntryDetailsFrame import EntryDetailsFrame


class DatabaseWidget(QWidget):
    UI_FILE = ROOT_DIR + "/ui/DatabaseWidget.ui"

    entrySelectionChanged = Signal(Entry)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(DatabaseWidget, self).__init__(parent)

        # Setup logging
        self.logger = logging.getLogger("Logger")

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self, {"EntryDetailsFrame": EntryDetailsFrame})
        self.ui.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.ui.tableView.setSortingEnabled(True)

        # Setup Model
        self.model = None

        # Setup SelectionModel
        self.selection_model = None

        # Connect Signals/Slots
        self.entrySelectionChanged.connect(self.ui.entryDetailsFrame.update_entry_information)

    @Slot()
    def database_changed(self):
        # Setup Model
        entries = []
        for entry in DBConnection.instance().query("SELECT * FROM Entries"):
            # Objekt für jeden Eintrag der Tabelle erstellen
            entries.append(Entry(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6]))

        self.model = TableModel(entries)
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.setColumnHidden(0, True)
        self.ui.tableView.selectRow(0)

        self.selection_model = self.ui.tableView.selectionModel()
        self.selection_model.selectionChanged.connect(self.selection_changed)
        self.selection_changed()

    @Slot()
    def selection_changed(self):
        self.entrySelectionChanged.emit(self.selected_entry())

    def selected_entry(self):
        if self.selection_model.hasSelection():
            index = self.selection_model.currentIndex()
            entry = self.model.entries[index.row()]
            return entry
        return None

    def delete_selected_entry(self):
        entry = self.selected_entry()
        self.delete_entry(entry)

    @Slot(Entry)
    def new_entry(self, entry: Entry):
        query = "INSERT INTO Entries  (title, username, password, url, notes, modified) VALUES (?, ?, ?, ?, ?, ?)"
        connection = DBConnection.instance()
        connection.execute(query, (entry.title, entry.username, entry.password, entry.url, entry.notes, entry.modified))
        entry.id = connection.cursor.lastrowid
        connection.commit()

        self.model.insertRow(0)

        # TODO: über Attribute iterieren

        # ID Setzen
        index = self.model.index(0, 0, QModelIndex())
        self.model.setData(index, entry.id, Qt.EditRole)

        # Titel setzen
        index = self.model.index(0, 1, QModelIndex())
        self.model.setData(index, entry.title, Qt.EditRole)

        # Benutzernamen setzen
        index = self.model.index(0, 2, QModelIndex())
        self.model.setData(index, entry.username, Qt.EditRole)

        # Passwort setzen
        index = self.model.index(0, 3, QModelIndex())
        self.model.setData(index, entry.password, Qt.EditRole)

        # URL setzen
        index = self.model.index(0, 4, QModelIndex())
        self.model.setData(index, entry.url, Qt.EditRole)

        # Notizen setzen
        index = self.model.index(0, 5, QModelIndex())
        self.model.setData(index, entry.notes, Qt.EditRole)

        # Zuletzt geändert setzen
        index = self.model.index(0, 6, QModelIndex())
        self.model.setData(index, entry.modified, Qt.EditRole)

        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.selectRow(0)

    @Slot(Entry)
    def edit_entry(self, entry: Entry) -> None:
        query = """
            UPDATE Entries
            SET title = ?, username = ?, password = ?, url = ?, notes = ?, modified = ?
            WHERE id = ?
            """
        connection = DBConnection.instance()
        connection.execute(query, (entry.title, entry.username, entry.password,
                                   entry.url, entry.notes, entry.modified, entry.id))
        connection.commit()

        self.entrySelectionChanged.emit(self.selected_entry())

    @Slot(Entry)
    def delete_entry(self, entry: Entry) -> None:
        try:
            row = self.model.entries.index(entry)
            self.model.removeRow(row)

            query = "DELETE FROM Entries WHERE id = ?"
            connection = DBConnection.instance()
            connection.execute(query, (entry.id,))
            connection.commit()
        except ValueError as e:
            self.logger.debug(f"Element {entry} nicht gefunden: {e}")
