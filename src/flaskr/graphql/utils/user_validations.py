import re


def validate_email(email):
    padrao_email = (
        r"^(?!-)(?!.*--)(?!.*\.$)[A-Za-z0-9-._%+]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )
    if re.match(padrao_email, email):
        return True
    return False
