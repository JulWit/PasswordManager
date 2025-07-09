import sys

from PySide6.QtWidgets import QApplication
from src.ui.MainWindow import MainWindow
from src.util.Theme import is_dark_theme_enabled
from src.util.Logger import logger


def main():
    """
    Startet die Anwendung.

    :return: None.
    """
    logger.debug("Logging gestartet")
    logger.debug(f"Dark mode: {is_dark_theme_enabled()}")

    app = QApplication(sys.argv)
    app.setApplicationName("Passwort Manager")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
