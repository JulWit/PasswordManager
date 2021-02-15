from dataclasses import dataclass
from datetime import datetime


@dataclass
class Entry:
    def __init__(self,
                 id: str = None,
                 title: str = None,
                 username: str = None,
                 password: str = None,
                 url: str = None,
                 notes: str = None,
                 modified: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')) -> None:
        self.id = id
        self.title = title
        self.username = username
        self.password = password
        self.url = url
        self.notes = notes
        self.modified = modified

    def __str__(self):
        return str(f"Entry[ID: {self.id}, Titel: {self.title}, Benutzername: {self.username}, "
                   f"Passwort: {self.password}, URL: {self.url}, Notizen: {self.notes}, "
                   f"Zuletzt geändert: {self.modified}]")
