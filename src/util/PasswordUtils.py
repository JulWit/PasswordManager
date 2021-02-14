import re
from password_strength import PasswordPolicy, PasswordStats

pw_regex = re.compile(r"^(?=.*[A-Z])(?=.*[\W])(?=.*[0-9])(?=.*[a-z]).{8,}$")

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=2,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)


def evaluate_password_strength(password: str) -> float:
    """ Bestimmt anhand von Entropy-Bits die Stärke eines Passworts, Werte zwischen 0 und 1 """
    if len(password) < 1:
        return 0
    return PasswordStats(password).strength()
