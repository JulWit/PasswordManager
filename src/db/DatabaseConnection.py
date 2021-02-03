import logging
import sqlcipher3


class DatabaseConnection:
    def __init__(self, file: str, password: str):
        if not file or not isinstance(file, str):
            raise TypeError("file is None or not a string")
        if not password or not isinstance(password, str):
            raise TypeError("password is None or not a string")

        # Setup logging
        self.logger = logging.getLogger('Logger')
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
            self.logger.error(f"Datenbank {file} konnte nicht entschlüsselt werden: {e}")
            raise e

        self.logger.debug(f"Datenbank {file} erfolgreich entschlüsselt")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
