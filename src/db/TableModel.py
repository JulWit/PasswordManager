import logging
import operator
from typing import Optional, List

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class TableModel(QAbstractTableModel):
    def __init__(self, data=None, parent=None):
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
            self._data = []
        else:
            self._data = data

    def data(self, index: QModelIndex, role: Qt.ItemDataRole = Qt.DisplayRole) -> List[str]:
        if role == Qt.DisplayRole:
            if index.column() == 3:
                return "*" * 8
            return self._data[index.row()][index.column()]

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, index: QModelIndex = QModelIndex()) -> int:
        return len(self._sections)

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: Qt.ItemDataRole = Qt.DisplayRole) -> Optional[str]:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._sections.get(section, None)
        return None

    def sort(self, column: int, order: Qt.SortOrder = Qt.AscendingOrder) -> None:
        self.layoutAboutToBeChanged.emit()
        self._data = sorted(self._data, key=operator.itemgetter(column))
        if order == Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()

    def removeRow(self, position: int, rows: int = 1, index: QModelIndex = QModelIndex()) -> bool:
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        del self._data[position:position + rows]
        self.endRemoveRows()
        return True
