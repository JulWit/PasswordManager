import string
import random

# globale Variablen für..
LETTERS = string.ascii_letters      # Buchstaben
NUMBERS = string.digits             # Zahlen
PUNCTUATION = string.punctuation    # Sonderzeichen

def get_password_length():
    # Mathode zum festlegen der Passwortlänge
    while True:
        length = input("Wie lang soll das Passwort sein?: ")

        try:
            return int(length)
            break
        except:
            print("Error: Bitte geben sie eine Zahl ein...")


def password_combination():
    # Methode zum erstellen einer benutzerdefinierten Struktur den generierten Passworts

    # Benutzereingabe: Benutzer entscheidet wie das Passwort aufgebaut ist
    stat_letters = input("Soll das Password Buchstaben enthalten?(True oder False): ")
    stat_digits = input("Soll das Password Zahlen enthalten?(True oder False): ")
    stat_punctuation = input("Soll das Password Sonderzeichen enthalten?(True oder False): ")

    # Benutzereingaben werden in Python Ausdrücke umgewandelt und zurueckgegeben
    try:
        stat_letters = eval(stat_letters.title())
        stat_digits = eval(stat_digits.title())
        stat_punctuation = eval(stat_punctuation.title())
        structure = [stat_letters, stat_digits, stat_punctuation]
    except NameError as e:
        print("Error: Bitte geben sie True oder False ein")
        print("Passwort wird mit Buchstaben, Zahlen und Sonderzeichen erstellt")
        structure = [True, True, True]

    # mögliche Zeichen für Passwort werden in einem string zusammengefasst
    string_printable = ''
    string_printable += LETTERS if structure[0] else ''
    string_printable += NUMBERS if structure[1] else ''
    string_printable += PUNCTUATION if structure[2] else ''

    return string_printable


def password_generator(length):
    # Methode zum generieren eines zufälligen Passworts
    printable = password_combination()

    printable = list(printable)
    random.shuffle(printable)

    password = random.choices(printable, k=length)
    password = ''.join(password)
    return password

# Test der Methoden
password_size = get_password_length()
random_password = password_generator(password_size)
print(random_password)