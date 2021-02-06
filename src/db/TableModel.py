from PySide6.QtCore import Qt, QAbstractTableModel


class TableModel(QAbstractTableModel):
    def __init__(self, data=None, parent=None):
        super(TableModel, self).__init__(parent)

    # TODO: Handle empty db
        if data is None:
            self._data = []
        else:
            self._data = data

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index=None):
        return len(self._data)

    def columnCount(self, index=None):
        # return len(self._data[0])
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
