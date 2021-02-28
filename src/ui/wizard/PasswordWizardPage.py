import re
from typing import Optional

from PySide6.QtWidgets import QWizardPage, QWidget

from src import ROOT_DIR
from src.ui import UiLoader
from src.util import PasswordStrength


class PasswordWizardPage(QWizardPage):
    """
    Seite eines Wizards für die Eingabe eines Passworts, dass für die Verschlüsselung der Datenbank genutzt wird.
    """

    # UI-Datei
    UI_FILE = ROOT_DIR + "/ui/PasswordWizardPage.ui"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues PasswordWizardPage-Objekt.

        :param parent: Übergeordnetes QWidget.
        """
        super(PasswordWizardPage, self).__init__(parent)

        # Setup Pattern
        self.pattern = re.compile(r"^[^\s]{1,128}$")

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)

        # Connect signals/slots
        self.ui.passwordLineEdit.textChanged.connect(self.password_changed)
        self.ui.passwordLineEdit.textChanged.connect(self.completeChanged)
        self.ui.confirmationLineEdit.textChanged.connect(self.completeChanged)

    def password(self) -> str:
        """
        Gibt das eingegebene Passwort zurück.

        :return: eingegebenes Passwort.
        """
        return self.ui.passwordLineEdit.text()

    def password_changed(self) -> None:
        """
        Beurteilt die Stärke des eingegebenen Passworts.

        :return: None.
        """
        strength = PasswordStrength.evaluate_password_strength(self.password())
        color = PasswordStrength.get_password_strength_category_color(strength)
        self.ui.passwordStrength.setStyleSheet("QProgressBar::chunk{background-color: " + color + "}")
        self.ui.passwordStrength.setValue(round(strength * 100, 0))

    def isComplete(self) -> bool:
        """
        Wird aufgerufen, wenn die eingegbenen Passwörter geändert wurden.
        Überprüft, ob die Passwörter gültig sind und deaktiviert ggf. den next-Button.

        :return: True, falls die Passwörter gültig sind, False sonst.
        """
        return bool(self.pattern.match(self.ui.passwordLineEdit.text()) and
                    self.pattern.match(self.ui.confirmationLineEdit.text()) and
                    self.ui.passwordLineEdit.text() == self.confirmationLineEdit.text())
