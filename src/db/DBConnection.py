import logging
import sqlcipher3

from typing import Optional, List
from sqlite3 import Connection, Cursor


class DBConnection(object):
    pass


class Singleton:
    _instance = None

    def __init__(self, class_name: type) -> None:
        self._class_name = class_name

    def __call__(self, *args: str, **kwargs: str) -> DBConnection:
        if Singleton._instance is None:
            Singleton._instance = self._class_name(*args, **kwargs)
        return Singleton._instance

    @classmethod
    def delete_instance(cls) -> None:
        cls._instance = None

    @classmethod
    def instance(cls) -> Optional[DBConnection]:
        return cls._instance


@Singleton
class DBConnection(object):
    def __init__(self, file: str, password: str) -> None:
        if not file  or not isinstance(file, str):
            raise TypeError("Datei ist None oder kein String")
        if not password or not isinstance(password, str):
            raise TypeError("Passwort ist None oder kein String")

        # Setup logging
        self.logger = logging.getLogger("Logger")
        self.logger.debug(f"Passwort: {password}")

        # Mit Datenbank verbinden und ggf. Datenbank erstellen
        self._connection = sqlcipher3.connect(file)
        self._cursor = self._connection.cursor()
        self._cursor.execute(f"PRAGMA KEY={password}")

        # Überprüfen, ob die Entschlüsselung funktioniert hat
        # SQLCipher bietet keine eigene Methode für die Überprüfung,
        # stattdessen wird eine Datenbankanfrage ausgeführt und Überprüft,
        # ob die Anfrage ohne Fehler ausgeführt wird
        try:
            self.execute("SELECT COUNT(*) FROM sqlite_master")
        except sqlcipher3.dbapi2.DatabaseError as e:
            self.close()
            self.logger.error(f"Die Datenbank {file} konnte nicht entschlüsselt werden: {e}")
            raise e

        self.logger.debug(f"Die Datenbank {file} wurde erfolgreich entschlüsselt")

    @property
    def connection(self) -> Connection:
        return self._connection

    @property
    def cursor(self) -> Cursor:
        return self._cursor

    def commit(self) -> None:
        self.connection.commit()

    def close(self, commit: bool = True) -> None:
        if commit:
            self.commit()
        self.connection.close()
        Singleton.delete_instance()

    def execute(self, sql, params: () = None) -> None:
        self.cursor.execute(sql, params or ())

    def fetch_all(self) -> List[List[str]]:
        return self.cursor.fetchall()

    def fetch_one(self) -> List[str]:
        return self.cursor.fetchone()

    def query(self, sql: str, params: () = None) -> List[List[str]]:
        self.cursor.execute(sql, params or ())
        return self.fetch_all()
