from dataclasses import dataclass


@dataclass
class DBData:
    """
    Metadaten einer SQLite Datenbank.
    """
    def __init__(self, name: str, password: str, description: str = None) -> None:
        """
        Initialisiert eine neues DBData-Objekt.

        :param name: Name der Datenbank.
        :param password: Passwort, welches für die Verschlüsselung der Datenbank genutzt wird.
        :param description: Beschreibung der Datenbank.
        """
        if not name or not isinstance(name, str):
            raise TypeError("Name ist None oder kein String")
        if not password or not isinstance(password, str):
            raise TypeError("Passwort ist Nonde oder kein String")
        if not isinstance(description, str):
            raise TypeError("Beschreibung ist kein String")

        self.name = name
        self.password = password
        self.description = description

    def __str__(self) -> str:
        """
        Gibt eine String-Repräsentation zurück.

        :return: DBData-Objekt als String.
        """
        return str(f"[DBData: Name: {self.name}, Passwort: {self.password} Beschreibung: {self.description}]")
