import logging
import sqlcipher3

from typing import List, Optional
from sqlite3 import Connection, Cursor


# Vorwärtsdeklaration
class DBConnection(object):
    pass


class Singleton:
    """
    Singeleton Dekorierer.

    :attributes:
        _instance: Einzige Instanz der dekorierten Klasse.
    """

    _instance = None

    def __init__(self, class_name: type) -> None:
        """
        Dekoriert die übergebene Klasse und erlaubt, dass nur eine Instanz der Klasse erzeugt werden kann.
        """
        self._class_name = class_name

    def __call__(self, *args: str, **kwargs: str) -> DBConnection:
        """
        Wird beim Aufruf der dekorierten Klasse aufgerufen. Gibt die einzige Instanz der dekorierten Klasse zurück.
        Falls keine Instanz existiert wird eine Instanz erzeugt.

        :param args: Argumente.
        :param kwargs: KeyWord-Argumente.
        :return: Einzige Instanz der dekorierten Klasse.
        """
        if Singleton._instance is None:
            Singleton._instance = self._class_name(*args, **kwargs)
        return Singleton._instance

    @classmethod
    def delete_instance(cls) -> None:
        """
        Entfent die einzige Instanz der Klasse.

        :return: None.
        """
        cls._instance = None

    @classmethod
    def instance(cls) -> Optional[DBConnection]:
        """
        Gibt die einzige Instanz der Klasse zurück, falls diese existiert.
        Existiert keine Instanz wird None zurückgegeben

        :return: Instanz der Klasse oder None.
        """
        return cls._instance


@Singleton
class DBConnection(object):
    """
    Verwaltet eine Verbindung zur Datenbank.
    Stellt ein connection- und ein cursor-Objekt für Datenbankanfragen zur Verfügung.
    """

    def __init__(self, file: str, password: str) -> None:
        """
        Initialisiert ein neues DBConnection-Objekt.

        :param file: Datenbankdatei.
        :param password: Passwort für die Entschlüsselung.
        """
        if not file or not isinstance(file, str):
            raise TypeError("Datei ist None oder kein String")
        if not password or not isinstance(password, str):
            raise TypeError("Passwort ist None oder kein String")

        # Setup logging
        self.logger = logging.getLogger("Logger")

        # Mit Datenbank verbinden und ggf. Datenbank erstellen
        self._connection = sqlcipher3.connect(file)
        self._cursor = self._connection.cursor()
        self._cursor.execute(f"PRAGMA KEY={password}")

        # Überprüfen, ob die Entschlüsselung funktioniert hat.
        # SQLCipher bietet keine eigene Methode für die Überprüfung,
        # stattdessen wird eine Datenbankanfrage ausgeführt. Falls diese Anfrage
        # ohne Fehler abläuft, wurde die Datenbank erfolgreich entschlüsselt
        try:
            self.execute("SELECT COUNT(*) FROM sqlite_master")
        except sqlcipher3.dbapi2.DatabaseError as e:
            self.close()
            self.logger.error(f"Die Datenbank {file} konnte nicht entschlüsselt werden: {e}")
            raise e
        self.logger.debug(f"Die Datenbank {file} wurde erfolgreich entschlüsselt")

    @property
    def connection(self) -> Connection:
        """
        Gibt das Connection-Objekt zurück.

        :return: Connection.
        """
        return self._connection

    @property
    def cursor(self) -> Cursor:
        """
        Gibt das Cursor-Objekt zurück.

        :return: Cursor.
        """
        return self._cursor

    def commit(self) -> None:
        """
        Commited auststehende Änderungen an der Datenabank.

        :return: None.
        """
        self._connection.commit()

    def close(self, commit: bool = True) -> None:
        """
        Schließt die bestehende Datenbankverbindung.

        :param commit: Bestimmt, ob ausstehende Änderungen vor dem Schließen commited werden sollen.
        :return: None.
        """
        if commit:
            self.commit()
        self._connection.close()
        Singleton.delete_instance()

    def execute(self, sql, params: () = None) -> None:
        """
        Führt das übergebene SQL-Statement aus.

        :param sql: SQL-Statement.
        :param params: Parameter für das SQL-Statement.
        :return: None.
        """
        self._cursor.execute(sql, params or ())

    def fetchall(self) -> List[List[str]]:
        """
        Gibt eine Ergebnisliste aller Einträge der zurletzt ausgeführten Anfrage zurück.

        :return: Ergebnisliste der Anfrage.
        """
        return self._cursor.fetchall()

    def fetchone(self) -> List[str]:
        """
        Gibt den ersten zur letzten ausgeführten Anfrage passenden Eintrag zurück.

        :return: Eintrag.
        """
        return self._cursor.fetchone()

    def query(self, sql: str, params: () = None) -> List[List[str]]:
        """
        Führt die übergebene SQL-Anfrage aus und gibt eine Ergebnisliste zurück.

        :param sql: SQL-Anfrage.
        :param params: Parameter für die SQL-Anfrage.
        :return: Ergebnisliste der Anfrage.
        """
        self._cursor.execute(sql, params or ())
        return self.fetchall()
