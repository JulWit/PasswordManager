from typing import Optional

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QWidget

from src.model.Entry import Entry
from src.ui.widget.EntryWidget import EntryWidget
from src.util.FaviconDownloader import download_favicon


class NewEntryWidget(EntryWidget):
    """
    Widget mit einer Maske für das Erstellen eines Eintrags.
    """

    # Signal, dass entsandt wird, wenn ein neuer Eintrag erstell wurde, Empfänger ist das DatabaseWidget
    entryCreated = Signal(Entry)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(NewEntryWidget, self).__init__(parent)

        # Setup UI
        self.ui.headerLabel.setText("Neuer Eintrag:")
        self.ui.okButton.setEnabled(False)

    @Slot()
    def on_okButton_clicked(self) -> None:
        """
        Wird aufgerufen, wenn der ok-Button geklickt wurde.
        Liest die Informationen aus der Maske aus und entsendet ein entryCreated-Signal mit dem neuem Eintrag.
        Entsendet darüber hinaus ein ok-Signal.

        :return: None
        """
        title = self.ui.titleLineEdit.text()
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        url = self.ui.urlLineEdit.text()
        notes = self.ui.notesTextEdit.toPlainText()
        icon = download_favicon(url)

        self.entryCreated.emit(Entry(None, title, username, password, url, notes, icon))
        self.ok.emit()
        self.clear()

    @Slot()
    def on_cancelButton_clicked(self) -> None:
        """
        Wird aufgerufen, wenn der abbrechen-Button geklickt wurde. Entsendet ein cancel-Signal.

        :return: None.
        """
        self.clear()
        self.cancel.emit()
