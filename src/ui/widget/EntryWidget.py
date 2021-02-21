from typing import Optional

from PySide6.QtCore import Signal, Slot, QMetaObject
from PySide6.QtWidgets import QWidget, QLineEdit
from src.__main__ import ROOT_DIR
from src.ui import UiLoader


class EntryWidget(QWidget):
    """
    Klasse, von der Widgets abgleitet sind, die eine Maske für das Erstellen oder Bearbeiten eines Eintrags benötigen.
    """

    # UI-Datei
    UI_FILE = ROOT_DIR + "/ui/EntryWidget.ui"

    # Signal, dass entsandt wird, wenn der ok-Button geklickt wurde
    ok = Signal()

    # Signal, dass entsandt wird, wenn der abbrechen-Button geklickt wurde
    cancel = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues EntryWidget-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(EntryWidget, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        # Connect signals/slots
        QMetaObject.connectSlotsByName(self)
        self.ui.titleLineEdit.textChanged.connect(self.title_changed)

    @Slot()
    def on_okButton_clicked(self) -> None:
        """
        Wird aufgerufen, wenn der ok-Button geklickt wurde.
        Muss durch abgeleitete Klassen überschrieben werden.

        :return: None
        """
        raise NotImplementedError("Die Methode on_okButton_clicked muss durch "
                                  "abgeleitete Klassen überschrieben werden")

    @Slot()
    def on_cancelButton_clicked(self) -> None:
        """
        Wird aufgerufen, wenn der abbrechen-Button geklickt wurde.
        Muss durch abgeleitete Klassen überschrieben werden.

        :return: None
        """
        raise NotImplementedError("Die Methode on_cancelButton_clicked muss durch "
                                  "abgeleitete Klassen überschrieben werden")

    @Slot()
    def title_changed(self) -> None:
        """
        Wird aufgerufen, wenn der Titel des Eintrags geändert wurde.
        Überprüft, ob der Titel nichtleer ist und deaktiviert ggf. den ok-Button.

        :return: None.
        """
        title = bool(self.ui.titleLineEdit.text().strip())
        self.ui.okButton.setEnabled(title)

    def clear(self) -> None:
        """
        Leert den Inhalt aller LineEdits.

        :return: None.
        """
        line_edits = self.ui.findChildren(QLineEdit)
        for line_edit in line_edits:
            line_edit.clear()
        self.ui.notesTextEdit.clear()
