from password_strength import PasswordStats


def evaluate_password_strength(password: str) -> float:
    """
    Bestimmt anhand von Entropy-Bits die Stärke eines Passworts, Werte zwischen 0 und 1

    :param password: Passwort.
    :return: Stärke des Passworts.
    """
    if len(password) < 1:
        return 0
    return PasswordStats(password).strength()


def get_password_strength_category_color(strength: float) -> str:
    """
    Stellt die Stärke eines Passworts farbig dar.
    :param strength: Stärke des Passworts von 0.0 bis 1.0
    :return: Darzustellende Farbe
    """
    color = "white"
    if 0 <= strength < 0.25:
        color = "red"
    if 0.25 < strength <= 0.50:
        color = "orange"
    elif 0.50 < strength <= 0.75:
        color = "MediumSeaGreen"
    elif 0.75 < strength <= 1:
        color = "green"
    return color
