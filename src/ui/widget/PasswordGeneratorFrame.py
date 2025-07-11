from typing import Optional

from PySide6.QtCore import Slot, QMetaObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QWidget, QApplication, QLineEdit

from src import ROOT_DIR
from src.ui import UiLoader
from src.util import PasswordStrength
from src.util.PasswordGenerator import password_combination, password_generator
from src.util.Theme import icon_path


class PasswordGeneratorFrame(QFrame):
    """
    Frame für das Generieren von Passwörtern.
    """

    # UI-Datei
    UI_FILE = ROOT_DIR + "/ui/PasswordGeneratorFrame.ui"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialisiert ein neues PasswordGeneratorFrame-Objekt.
        """
        super(PasswordGeneratorFrame, self).__init__(parent)

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.ui.echoButton.setIcon(QIcon(str(icon_path / "eye.svg")))
        self.ui.refreshButton.setIcon(QIcon(str(icon_path / "refresh.svg")))
        self.ui.copyToClipboardButton.setIcon(QIcon(str(icon_path / "copy-text.svg")))

        # Connect signals / slots
        QMetaObject.connectSlotsByName(self)
        self.ui.passwordLineEdit.textChanged.connect(self.refresh_password_strength)
        self.ui.passwordLineEdit.textChanged.connect(self.password_changed)

        # Passwortlänge
        self.ui.passwordLengthSlider.valueChanged.connect(self.new_password)
        self.ui.passwordLengthSlider.valueChanged.connect(self.refresh_password_length_label)

        # CheckBoxen
        self.ui.capitalLettersCheckBox.stateChanged.connect(self.new_password)
        self.ui.numbersCheckBox.stateChanged.connect(self.new_password)
        self.ui.spacesCheckBox.stateChanged.connect(self.new_password)
        self.ui.specialCharactersCheckBox.stateChanged.connect(self.new_password)
        self.ui.bracketsCheckBox.stateChanged.connect(self.new_password)

        # Standardwerte
        self.password = None
        self.included_characters = None
        self.password_length = None

        self.refresh_included_characters()
        self.refresh_password_length_slider()
        self.new_password()

    @Slot()
    def password_changed(self) -> None:
        self.password = self.ui.passwordLineEdit.text()

    @Slot()
    def new_password(self) -> None:
        """
        Erzeugt ein neues Passwort unter Berücksichtigung der Vorgaben
        :return: None
        """
        self.refresh_password_length_slider()
        self.refresh_included_characters()

        self.password = password_generator(self.password_length, self.included_characters)
        self.ui.passwordLineEdit.setText(self.password)

    @Slot()
    def refresh_password_strength(self) -> None:
        """
        Beurteilt die Stärke des eingegebenen Passworts.

        :return: None.
        """
        strength = PasswordStrength.evaluate_password_strength(self.password)
        color = PasswordStrength.get_password_strength_category_color(strength)
        self.ui.passwordStrengthProgressBar.setStyleSheet("QProgressBar::chunk{background-color: " + color + "}")
        self.ui.passwordStrengthProgressBar.setValue(round(strength * 100, 0))

    @Slot()
    def refresh_password_length_label(self) -> None:
        """
        Aktualisiert die Anzeige für die Länge des zu generierenden Passworts
        :return: None
        """
        self.ui.passwordLengthLabel.setText(str(self.password_length))

    @Slot()
    def refresh_password_length_slider(self) -> None:
        """
        Aktualisiert die Anzahl von Zeichen anhand der Sliderposition, die das generierte Passwort haben soll.
        :return: None
        """
        self.password_length = self.ui.passwordLengthSlider.value()

    @Slot()
    def refresh_included_characters(self) -> None:
        """
        Aktualisiert die Liste der für die Passwort generierung zu verwendenden Zeichen.
        :return:  None
        """
        self.included_characters = password_combination(self.ui.capitalLettersCheckBox.isChecked(),
                                                        self.ui.numbersCheckBox.isChecked(),
                                                        self.ui.spacesCheckBox.isChecked(),
                                                        self.ui.specialCharactersCheckBox.isChecked(),
                                                        self.ui.bracketsCheckBox.isChecked())

    @Slot()
    def on_refreshButton_clicked(self) -> None:
        """
        Generiert bei einem Button-click auf refresh ein neues Passwort unter Beachtung der Vorgaben
        :return: None
        """
        self.new_password()

    @Slot()
    def on_copyToClipboardButton_clicked(self) -> None:
        """
        Kopiert das generierte Passwort in die Zwischenablage
        :return: None
        """
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password)

    @Slot()
    def on_echoButton_clicked(self) -> None:
        """
        Wechselt zwischen der Anzeigen des Passworts in Klartext oder der Anzeige des unkenntlich gemachten Passworts.
        :return:
        """
        lineEdit = self.ui.passwordLineEdit
        if lineEdit.echoMode() == QLineEdit.EchoMode.Password:
            lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.echoButton.setIcon(QIcon(str(icon_path / "eye-off.svg")))
        else:
            lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.echoButton.setIcon(QIcon(str(icon_path / "eye.svg")))
