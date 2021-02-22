from typing import Optional

from PySide6.QtCore import Slot, QMetaObject
from PySide6.QtWidgets import QFrame, QWidget, QApplication, QLineEdit

from src.__main__ import ROOT_DIR
from src.ui import UiLoader
from src.util import PasswordUtils
from src.util.PasswordGenerator import password_combination, password_generator


class PasswordGeneratorFrame(QFrame):
    """
    Frame für das generieren von Passwörtern.
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
        self.ui.passwordLineEdit.textChanged.connect(self.refresh_password_strength)

        # Connect signals / slots
        QMetaObject.connectSlotsByName(self)

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
    def new_password(self) -> None:
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
        strength = PasswordUtils.evaluate_password_strength(self.password)
        color = "white"
        if 0 <= strength < 0.25:
            color = "red"
        if 0.25 < strength < 0.50:
            color = "orange"
        elif 0.50 < strength < 0.75:
            color = "MediumSeaGreen"
        elif 0.75 < strength <= 1:
            color = "green"
        self.ui.passwordStrengthProgressBar.setStyleSheet("QProgressBar::chunk{background-color: " + color + "}")
        self.ui.passwordStrengthProgressBar.setValue(round(strength * 100, 0))

    @Slot()
    def refresh_password_length_label(self) -> None:
        self.ui.passwordLengthLabel.setText(str(self.password_length))

    @Slot()
    def refresh_password_length_slider(self) -> None:
        self.password_length = self.ui.passwordLengthSlider.value()

    @Slot()
    def refresh_included_characters(self) -> None:
        self.included_characters = password_combination(self.ui.capitalLettersCheckBox.isChecked(),
                                                        self.ui.numbersCheckBox.isChecked(),
                                                        self.ui.spacesCheckBox.isChecked(),
                                                        self.ui.specialCharactersCheckBox.isChecked(),
                                                        self.ui.bracketsCheckBox.isChecked())

    @Slot()
    def on_refreshButton_clicked(self) -> None:
        self.new_password()

    @Slot()
    def on_copyToClipboardButton_clicked(self) -> None:
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password)

    @Slot()
    def on_echoButton_toggled(self) -> None:
        if self.ui.echoButton.isChecked():
            self.ui.passwordLineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.passwordLineEdit.setEchoMode(QLineEdit.Password)