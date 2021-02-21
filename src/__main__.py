import os
import PasswordManager

# Root-Verzeichnis der Anwendung
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

if __name__ == '__main__':
    """
    Startet die Anwendung.
    """
    PasswordManager.main()
