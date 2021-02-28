from datetime import datetime
from typing import Optional

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QWidget

from src.model.Entry import Entry
from src.ui.widget.EntryWidget import EntryWidget
from src.util.FaviconDownloader import download_favicon


class EditEntryWidget(EntryWidget):
    """
    Widget mit einer Maske für das Bearbeiten eines Eintrags.
    """

    # Signal, dass entsandt wird, wenn ein Eintrag geändert wurde, Empfänger ist das DatabaseWidget
    entryEdited = Signal(Entry)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues EditEntryWidget-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(EditEntryWidget, self).__init__(parent)

        # Eintrag
        self._entry = None

        # Setup UI
        self.ui.headerLabel.setText("Eintrag bearbeiten:")

    @Slot()
    def on_okButton_clicked(self) -> None:
        """
        Wird aufgerufen, wenn der ok-Button geklickt wurde.
        Liest die Informationen aus der Maske aus und entsendet ein entryEdited-Signal mit dem geänderten Eintrag.
        Entsendet darüber hinaus ein ok-Signal.

        :return: None
        """
        self._entry.title = self.ui.titleLineEdit.text()
        self._entry.username = self.ui.usernameLineEdit.text()
        self._entry.password = self.ui.passwordLineEdit.text()
        self._entry.url = self.ui.urlLineEdit.text()
        self._entry.notes = self.ui.notesTextEdit.toPlainText()
        self._entry.icon = download_favicon(self._entry.url)
        self._entry.modified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.entryEdited.emit(self._entry)
        self.ok.emit()

    @Slot()
    def on_cancelButton_clicked(self) -> None:
        """
        Wird aufgerufen, wenn der abbrechen-Button geklickt wurde. Entsendet ein cancel-Signal.

        :return: None.
        """
        self.cancel.emit()

    @Slot(Entry)
    def entry_changed(self, entry: Entry) -> None:
        """
        Wird aufgerufen, wenn der in der TableView ausgewählte Eintrag geängert wurde.
        Aktualisiert den Eintrag des Widgets.

        :param entry: Ausgewählter Eintrag.
        :return: None.
        """
        self._entry = entry
        if entry is not None:
            self.ui.titleLineEdit.setText(entry.title)
            self.ui.usernameLineEdit.setText(entry.username)
            self.ui.passwordLineEdit.setText(entry.password)
            self.ui.urlLineEdit.setText(entry.url)
            self.ui.notesTextEdit.setPlainText(entry.notes)
        else:
            self.clear()
