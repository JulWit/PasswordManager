from dataclasses import dataclass
from datetime import datetime

from PySide6.QtCore import QByteArray


@dataclass
class Entry:
    """
    Eintrag in der Datenbank des Passwort-Managers.
    """
    def __init__(self, id: str = None, title: str = None, username: str = None,
                 password: str = None, url: str = None, notes: str = None,
                 icon: QByteArray = None,
                 modified: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')) -> None:
        """
        Initialisiert ein neues Entry-Objekt.

        :param id: ID des Eintrags.
        :param title: Titel des Eintrags.
        :param username: Benutzername des Eintrags.
        :param password: Passwort des Eintrags.
        :param url: URL des Eintrags.
        :param notes: Notizen des Eintrags.
        :param icon: Icon der Webseite des Eintags.
        :param modified: Änderungszeitpunkt des Eintrags.
        """
        self.id = id
        self.title = title
        self.username = username
        self.password = password
        self.url = url
        self.notes = notes
        self.icon = icon
        self.modified = modified

    def __str__(self) -> str:
        """
        Gibt eine String-Repräsentation zurück.

        :return: Entry-Objekt als String.
        """
        return str(f"Entry[ID: {self.id}, Titel: {self.title}, Benutzername: {self.username}, "
                   f"Passwort: {self.password}, URL: {self.url}, Notizen: {self.notes}, "
                   f"Zuletzt geändert: {self.modified}]")
