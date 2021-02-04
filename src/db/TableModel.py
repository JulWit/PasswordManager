from PySide6.QtCore import Qt, QAbstractTableModel


class TableModel(QAbstractTableModel):
    def __init__(self, data=None, parent=None):
        super(TableModel, self).__init__(parent)

    # TODO: Handle empty db
        if data is None:
            self._data = []
        else:
            self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "ID"
            elif section == 1:
                return "Title"
            elif section == 2:
                return "Username"
            elif section == 3:
                return "Password"
            elif section == 4:
                return "URL"
            elif section == 5:
                return "Notes"
            elif section == 6:
                return "Date"
        return None
