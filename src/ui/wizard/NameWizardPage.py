import re
from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWizardPage, QWidget

from src import ROOT_DIR
from src.ui import UiLoader


class NameWizardPage(QWizardPage):
    """
    Seite eines Wizards für die Eingabe eines Datenbanknamens und einer Beschreibung.
    """

    # UI-Datei
    UI_FILE = ROOT_DIR + "/ui/NameWizardPage.ui"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues NameWizardPage-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(NameWizardPage, self).__init__(parent)

        # Setup Pattern
        self.pattern = re.compile(r"^\S{1,128}$")

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        # Connect signals/slots
        self.ui.nameLineEdit.textChanged.connect(self.completeChanged)

    def name(self) -> str:
        """
        Gibt den eingegebenen Datenbanknamen zurück.

        :return: Datenbankname.
        """
        return self.ui.nameLineEdit.text()

    def description(self) -> str:
        """
        Gibt die eingegebene Datenbankbeschreibung zurück.

        :return: Datenbankbeschreibung.
        """
        return self.descriptionLineEdit.text()

    @Slot()
    def isComplete(self) -> bool:
        """
        Wird aufgerufen, wenn der Datenbankname geändert wurde.
        Überprüft, ob der Datenbankname gültig ist und deaktiviert ggf. den next-Button.

        :return: True, falls der Datenbankname gültig ist, False sonst.
        """
        return bool(self.pattern.match(self.ui.nameLineEdit.text()))


