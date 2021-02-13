import logging
import operator

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex


class TableModel(QAbstractTableModel):
    def __init__(self, data=None, parent=None):
        super(TableModel, self).__init__(parent)

        # Setup logging
        self.logger = logging.getLogger('Logger')

        if data is None:
            self._data = []
        else:
            self._data = data

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        # return len(self._data[0])\
        return 7

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "ID"
            elif section == 1:
                return "Titel"
            elif section == 2:
                return "Benutzername"
            elif section == 3:
                return "Passwort"
            elif section == 4:
                return "URL"
            elif section == 5:
                return "Notizen"
            elif section == 6:
                return "Zuletzt geändert"
        return None

    def sort(self, column, order=Qt.AscendingOrder):
        self.layoutAboutToBeChanged.emit()
        self._data = sorted(self._data, key=operator.itemgetter(column))
        if order == Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()

    def removeRow(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        del self._data[position:position+rows]
        self.endRemoveRows()
        return True
