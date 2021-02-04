import re
from zxcvbn import zxcvbn

pw_regex = re.compile(r"^(?=.*[A-Z].*[A-Z])(?=.*[\W])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,}$")


def evaluate_password(password):
    # results = zxcvbn(password, user_inputs=[])
    # print(results["score"])

    # TODO: Make pretty

    if len(password) < 8:
        return 0
    strength = 0
    if len(password) < 8:
        return 0
    # space, newline, tab etc. nicht zulässig
    if re.search("\s", password):
        return 0

    if len(re.findall("[a-z]", password)) > 0:
        strength = strength + 0.1

    if len(re.findall("[A-Z]", password)) > 0:
        strength = strength + 0.1

    if len(re.findall("[0-9]", password)) > 0:
        strength = strength + 0.1

    if len(re.findall("[\W]", password)) > 0:
        strength = strength + 0.2

    if len(password) > 10:
        strength = strength + 0.1

    if len(re.findall("[\W]", password)) > 2:
        strength = strength + 0.2

    if len(re.findall("[A-Z]", password)) > 2:
        strength = strength + 0.1

    if len(password) > 15:
        strength = strength + 0.1

    return strength
