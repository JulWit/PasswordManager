import string
import random

LETTERS = string.ascii_letters
NUMBERS = string.digits
PUNCTUATION = string.punctuation

def get_password_length():
    length = input("Wie lang soll das Passwort sein: ")
    return int(length)

def password_generator(length):
    # create alphanumerical from string constants
    printable = f'{LETTERS}{NUMBERS}{PUNCTUATION}'

    printable = list(printable)
    random.shuffle(printable)

    password = random.choices(printable, k=length)
    password = ''.join(password)
    return password

password_size = get_password_length()
random_password = password_generator(password_size)
print(random_password)