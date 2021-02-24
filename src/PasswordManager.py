import sys

from PySide6.QtWidgets import QApplication
from src.util import Logger
from src.ui.MainWindow import MainWindow


def main():
    """
    Startet die Anwendung.

    :return: None.
    """
    logger = Logger.setup_logger("Logger")
    logger.debug("Logging gestartet")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
