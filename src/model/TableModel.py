import logging

from typing import Optional, List
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QByteArray
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QWidget

from src.model.Entry import Entry


class TableModel(QAbstractTableModel):
    """
    Datenmodell der TableView
    """

    def __init__(self, data: List[Entry] = None, parent: Optional[QWidget] = None):
        """
        Initialisiert ein neues TableModel-Objekt.

        :param data: Daten des Models.
        :param parent: Übergeordnetes QWidget.
        """
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

    def data(self, index: QModelIndex, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Optional[str] | QIcon:
        """
        Gibt die Daten für die übergebene Rolle am übergebenen Index zurück.

        :param index: Index der Daten.
        :param role: Rolle der Daten.
        :return: Daten am übergebenen Index mit der übergebenen Rolle als String.
        Falls am übergebenen Index keine Daten existieren, wird None zurückgegeben.
        """
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self._data):
            return None

        if role == Qt.ItemDataRole.DecorationRole:
            entry = self._data[index.row()]
            if index.column() == 1:
                pixmap = QPixmap()
                pixmap.loadFromData(entry.icon)
                return QIcon(pixmap)
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            entry = self._data[index.row()]
            if index.column() == 0:
                return entry.id
            elif index.column() == 1:
                return entry.title
            elif index.column() == 2:
                return entry.username
            elif index.column() == 3:
                if len(entry.password) > 0:
                    return "*" * 8
                else:
                    return ""
            elif index.column() == 4:
                return entry.url
            elif index.column() == 5:
                return entry.notes
            elif index.column() == 6:
                return entry.modified
        return None

    def setData(self, index: QModelIndex, value: str | QByteArray, role: Qt.ItemDataRole = Qt.ItemDataRole.EditRole) -> bool:
        """
        Setzt die Daten für die übergebene Rolle am übergebenen Index.

        :param index: Index der Daten.
        :param value: Neuer Wert der Daten.
        :param role: Rolle der Daten.
        :return: True, falls das Setzen funktioniert hat, false sonst.
        """

        if role == Qt.ItemDataRole.DecorationRole:
            entry = self._data[index.row()]
            if index.column() == 1:
                entry.icon = value
            return False

        if role == Qt.ItemDataRole.EditRole:
            if index.isValid() and 0 <= index.row() < len(self._data):
                entry = self._data[index.row()]
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
                return True
        return False

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        Gibt die Anzahl der Zeilen unter dem übergebenen parent zurück.
        Ist der parent gültig, so wird die Anzahl der Kinder des parent zurückgegeben.

        :param parent: parent-Element.
        :return: Anzahl der Zeilen.
        """
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        Gibt die Anzahl der Spalten unter dem übergebenen parent zurück.

        :param parent: parent-Element.
        :return: Anzahl der Spalten.
        """
        return len(self._sections)

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Optional[str]:
        """
        Gibt die Daten für die übergebene Rolle und Sektion im Header mit der übergebenen Orientierung zurück.

        :param section: Sektion der Daten.
        :param orientation: Orientierung des Headers.
        :param role: Rolle der Daten.
        :return: Daten für die übergebene Rolle und Sektion im Header mit der übergebenen Orientierung.
        """
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self._sections[section]
        return None

    def insertRows(self, position: int, rows: int = 1, parent: QModelIndex = QModelIndex()) -> bool:
        """
        Fügt die übergebene Anzahl von Zeilen vor der übergebenen Position ein.
        Die neu eingefügten Zeilen werden zu Kindern des übergebenen parent-Elements.

        :param position: Position, vor der die Zeilen eingefügt werden sollen.
        :param rows: Anzahl der einzufügenden Zeilen.
        :param parent: parent-Element.
        :return: True, wenn das Einfügen funktioniert hat.
        """
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self._data.insert(position + row, Entry())
        self.endInsertRows()
        return True

    def removeRows(self, position: int, rows: int = 1, parent: QModelIndex = QModelIndex()) -> bool:
        """
        Entfernt die übergebene Anzahl von Zeilen beginnend ab der übergebenen Position 
        unter dem übergebenen parent-Element.
        
        :param position: Position, ab der die Zeilen entfernt werden sollen.
        :param rows: Anzahl der zu entfernenden Zeilen.
        :param parent: parent-Element.
        :return: True, wenn das Entfernen funktioniert hat.
        """
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        del self._data[position:position + rows]
        self.endRemoveRows()
        return True
