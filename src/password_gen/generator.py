import string
import random

# globale Variablen für..
LETTERS = string.ascii_letters      # Buchstaben
NUMBERS = string.digits             # Zahlen
PUNCTUATION = string.punctuation    # Sonderzeichen

# Mathode zum festlegen der Passwortlänge
def get_password_length():
    while True:
        length = input("Wie lang soll das Passwort sein: ")

        try:
            return int(length)
            break
        except:
            print("Error: Bitte geben sie eine Zahl ein...")

# Methode zum generieren eines zufälligen Passworts
def password_generator(length):
    printable = f'{LETTERS}{NUMBERS}{PUNCTUATION}'

    printable = list(printable)
    random.shuffle(printable)

    password = random.choices(printable, k=length)
    password = ''.join(password)
    return password

# Test der Methoden
password_size = get_password_length()
random_password = password_generator(password_size)
print(random_password)