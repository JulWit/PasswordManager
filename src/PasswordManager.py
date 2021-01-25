import sys
from PySide6.QtWidgets import QApplication
from src.ui.MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
