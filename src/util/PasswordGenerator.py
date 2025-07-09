import string
import secrets
import random
from typing import List


def password_combination(capital_letters: bool, numbers: bool, spaces: bool, special_characters: bool,
                         brackets: bool) -> List[str]:
    """
    Erstellt eine Zeichenliste für die Passwortgenerierung basierend auf benutzerdefinierten Optionen.

    Die Funktion berücksichtigt verschiedene Zeichentypen (Großbuchstaben, Zahlen, Leerzeichen,
    Sonderzeichen, Klammern) und erstellt daraus eine zufällig durchmischte Liste von Zeichen,
    die bei der Passwortgenerierung verwendet werden kann.

    :param capital_letters: Ob Großbuchstaben (`A-Z`) enthalten sein sollen.
    :param numbers: Ob Ziffern (`0-9`) enthalten sein sollen.
    :param spaces: Ob Leerzeichen enthalten sein sollen.
    :param special_characters: Ob Sonderzeichen (`#$%@^`~`) enthalten sein sollen.
    :param brackets: Ob Klammern (`[{(<>)}]`) enthalten sein sollen.
    :return: Eine zufällig sortierte Liste aller eingeschlossenen Zeichen.
    """
    # Methode zum Erstellen einer benutzerdefinierten Struktur des generierten Passworts
    string_printable = string.ascii_lowercase

    if capital_letters:
        string_printable += string.ascii_uppercase

    if numbers:
        string_printable += string.digits

    if spaces:
        string_printable += " "

    if special_characters:
        string_printable += "#$%@^`~"

    if brackets:
        string_printable += "[{(<>)}]"

    included_characters_list = list(string_printable)
    random.shuffle(included_characters_list)

    return included_characters_list


def password_generator(length, included_characters) -> str:
    """
    Generiert ein sicheres, zufälliges Passwort aus einer gegebenen Zeichenauswahl.

    Die Funktion erstellt ein Passwort der gewünschten Länge auf Basis der übergebenen Zeichenliste.

    :param length: Die gewünschte Passwortlänge.
    :param included_characters: Liste der zulässigen Zeichen für das Passwort.
    :return: Das generierte Passwort als Zeichenkette.
    """
    password = ''.join(secrets.choice(included_characters) for i in range(length))
    return password
