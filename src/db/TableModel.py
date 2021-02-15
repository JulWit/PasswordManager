import logging
import operator

from typing import Optional
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import QWidget

from src.db.Entry import Entry


class TableModel(QAbstractTableModel):
    def __init__(self, data=None, parent: Optional[QWidget] = None):
        super(TableModel, self).__init__(parent)

        # Setup logging
        self.logger = logging.getLogger("Logger")

        # Sections
        self._sections = {
            0: "ID",
            1: "Titel",
            2: "Benutzername",
            3: "Passwort",
            4: "URL",
            5: "Notizen",
            6: "Zuletzt geändert"
        }

        if data is None:
            self.entries = []
        else:
            self.entries = data

    def data(self, index: QModelIndex, role: Qt.ItemDataRole = Qt.DisplayRole):
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self.entries):
            return None

        if role == Qt.DisplayRole:
            entry = self.entries[index.row()]
            if index.column() == 0:
                return entry.id
            elif index.column() == 1:
                return entry.title
            elif index.column() == 2:
                return entry.username
            elif index.column() == 3:
                return "*" * 8
            elif index.column() == 4:
                return entry.url
            elif index.column() == 5:
                return entry.notes
            elif index.column() == 6:
                return entry.modified
        return None

    def setData(self, index: QModelIndex, value: str, role: Qt.ItemDataRole = Qt.EditRole):
        if role != Qt.EditRole:
            return False

        if index.isValid() and 0 <= index.row() < len(self.entries):
            entry = self.entries[index.row()]
            if index.column() == 0:
                entry.id = value
            elif index.column() == 1:
                entry.title = value
            elif index.column() == 2:
                entry.username = value
            elif index.column() == 3:
                entry.password = value
            elif index.column() == 4:
                entry.url = value
            elif index.column() == 5:
                entry.notes = value
            elif index.column() == 6:
                entry.modified = value
            self.dataChanged.emit(index, index)

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        return len(self.entries)

    def columnCount(self, index: QModelIndex = QModelIndex()) -> int:
        return len(self._sections)

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: Qt.ItemDataRole = Qt.DisplayRole) -> Optional[str]:
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self._sections[section]

        return None

    def sort(self, column: int, order: Qt.SortOrder = Qt.AscendingOrder) -> None:
        self.layoutAboutToBeChanged.emit()

        key = "id"
        if column == 0:
            key = "id"
        elif column == 1:
            key = "title"
        elif column == 2:
            key = "username"
        elif column == 3:
            key = "password"
        elif column == 4:
            key = "url"
        elif column == 5:
            key = "notes"
        elif column == 6:
            key = "modified"

        self.entries = sorted(self.entries, key=operator.attrgetter(key))
        if order == Qt.DescendingOrder:
            self.entries.reverse()
        self.layoutChanged.emit()

    def insertRows(self, position, rows=1, index=QModelIndex()) -> bool:
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.entries.insert(position + row, Entry())
        self.endInsertRows()
        return True

    def removeRows(self, position: int, rows: int = 1, index: QModelIndex = QModelIndex()) -> bool:
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        del self.entries[position:position + rows]
        self.endRemoveRows()
        return True
