import string
import secrets
import random


def password_combination(capital_letters: bool, numbers: bool, spaces: bool, special_characters: bool, brackets: bool):
    # Methode zum erstellen einer benutzerdefinierten Struktur den generierten Passworts

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


def password_generator(length, included_characters):
    # Methode zum generieren eines zufälligen Passworts

    password = ''.join(secrets.choice(included_characters) for i in range(length))
    return password
