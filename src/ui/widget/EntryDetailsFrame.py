from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QFrame, QWidget, QLabel

from src.__main__ import ROOT_DIR
from src.db.Entry import Entry
from src.ui import UiLoader


class EntryDetailsFrame(QFrame):
    """
    Frame mit Details zu einem ausgewählten Eintrag.
    """

    # UI-Datei
    UI_FILE = ROOT_DIR + "/ui/EntryDetailsFrame.ui"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues EntryDetailsFrame-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(EntryDetailsFrame, self).__init__(parent)

        # Eintrag
        self._entry = None

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

    @Slot()
    def entry_changed(self, entry: Entry):
        """
        Wird aufgerufen, wenn der in der TableView ausgewählte Eintrag geängert wurde.
        Aktualisiert den Eintrag des Widgets.

        :param entry: Ausgewählter Eintrag.
        :return: None.
        """
        self._entry = entry
        if entry is not None:
            self.ui.titleLabel.setText(entry.title)
            self.ui.usernameLabel.setText(entry.username)
            self.ui.passwordLabel.setText(entry.password)
            self.ui.urlLabel.setText(entry.url)
            self.ui.notesLabel.setText(entry.notes)

            pixmap = QPixmap()
            pixmap.loadFromData(entry.icon, "")
            self.ui.iconLabel.setPixmap(pixmap)
        else:
            labels = self.ui.findChildren(QLabel)
            for label in labels:
                label.clear()

