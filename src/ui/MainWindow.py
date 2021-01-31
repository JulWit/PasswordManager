import sys

from PySide6.QtCore import Slot, QMetaObject, QDir
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QFileDialog

from src.__main__ import ROOT_DIR
from src.ui.WelcomeWidget import WelcomeWidget
from src.ui.wizard.NewDatabaseWizard import NewDatabaseWizard
from src.ui import UiLoader


class MainWindow(QMainWindow):
    UI_FILE = ROOT_DIR + "/ui/MainWindow.ui"
    ICON_FILE = ROOT_DIR + "/img/logo.png"

    def __init__(self):
        super(MainWindow, self).__init__()

        # Setup UI
        self.ui = UiLoader.loadUi(self.UI_FILE, self)
        self.central_widget = WelcomeWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setWindowIcon(QIcon(self.ICON_FILE))

        # Connect Signals / Slots
        QMetaObject.connectSlotsByName(self)
        QMetaObject.connectSlotsByName(self.central_widget)

    @Slot()
    def on_actionNewDatabase_triggered(self) -> None:
        self.create_new_database()

    @Slot()
    def on_actionOpenDatabase_triggered(self) -> None:
        self.open_database()

    @Slot()
    def on_actionExit_triggered(self) -> None:
        sys.exit()

    @Slot()
    def on_newDatabaseButton_clicked(self) -> None:
        self.create_new_database()

    @Slot()
    def on_openDatabaseButton_clicked(self) -> None:
        self.open_database()

    def create_new_database(self) -> None:
        wizard = NewDatabaseWizard(self)
        if wizard.exec_():
            data = wizard.get_database_data()
            url = QFileDialog.getSaveFileName(self,
                                              self.tr("Datenbank speichern"),
                                              QDir.homePath() + "/" + data.name + ".db")

    def open_database(self) -> None:
        dialog = QFileDialog(self,
                             self.tr("Datenbank öffnen"),
                             QDir.homePath(),
                             self.tr("Datenbank Dateien (*.db)"))
        dialog.exec_()
