def has_lowercase(password: str) -> bool:
    """Return True if password contains at least one letter a-z."""
    raise NotImplementedError


def has_uppercase(password: str) -> bool:
    """Return True if password contains at least one letter A-Z."""
    raise NotImplementedError


def has_digit(password: str) -> bool:
    """Return True if password contains at least one digit 0-9."""
    raise NotImplementedError


def has_symbol(password: str) -> bool:
    """Return True if password contains a character that is not a-z, A-Z or 0-9 (spaces count)."""
    raise NotImplementedError


def password_strength(password: str) -> dict:
    """Return {"score": 0..6, "label": "weak" / "medium" / "strong"} built from the helpers above."""
    raise NotImplementedError
