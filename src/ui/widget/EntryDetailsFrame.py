from typing import Optional

from PySide6.QtCore import Slot, QMetaObject
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QWidget, QLabel

from src import ROOT_DIR
from src.model.Entry import Entry
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

        # Connect Signals/Slots
        QMetaObject.connectSlotsByName(self)

    @Slot()
    def entry_changed(self, entry: Entry):
        """
        Wird aufgerufen, wenn der in der TableView ausgewählte Eintrag geängert wurde.
        Aktualisiert den Eintrag des Widgets.

        :param entry: Ausgewählter Eintrag.
        :return: None.
        """
        self._entry = entry
        self.ui.echoButton.setChecked(False)
        if entry is not None:
            self.ui.titleLabel.setText(entry.title)
            self.ui.usernameLabel.setText(entry.username)
            self.ui.passwordLabel.setText("*" * len(entry.password))
            self.ui.urlLabel.setText(entry.url)
            self.ui.notesLabel.setText(entry.notes)

            pixmap = QPixmap()
            pixmap.loadFromData(entry.icon, "")
            self.ui.iconLabel.setPixmap(pixmap)
        else:
            self.clear_details()

    @Slot()
    def clear_details(self) -> None:
        self.ui.titleLabel.clear()
        self.ui.usernameLabel.clear()
        self.ui.passwordLabel.clear()
        self.ui.urlLabel.clear()
        self.ui.notesLabel.clear()

        pixmap = QPixmap(ROOT_DIR + "/img/globe.svg")
        self.ui.iconLabel.setPixmap(pixmap)


    @Slot()
    def on_echoButton_clicked(self) -> None:
        """
        Wird aufgerufen, wenn der echo-Button geklickt wurde.
        Ändert den echo-Mode des Passwort-Labels.

        :return: None.
        """
        if self.ui.echoButton.isChecked():
            self.ui.passwordLabel.setText(self._entry.password)
        else:
            self.ui.passwordLabel.setText("*" * len(self._entry.password))
