# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def is_lower(ch: str) -> bool:
    return "a" <= ch <= "z"


def is_upper(ch: str) -> bool:
    return "A" <= ch <= "Z"


def is_digit(ch: str) -> bool:
    return "0" <= ch <= "9"


def has_lowercase(password: str) -> bool:
    for ch in password:
        if is_lower(ch):
            return True
    return False


def has_uppercase(password: str) -> bool:
    for ch in password:
        if is_upper(ch):
            return True
    return False


def has_digit(password: str) -> bool:
    for ch in password:
        if is_digit(ch):
            return True
    return False


def has_symbol(password: str) -> bool:
    for ch in password:
        if not is_lower(ch) and not is_upper(ch) and not is_digit(ch):
            return True
    return False


def password_strength(password: str) -> dict:
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if has_lowercase(password):
        score += 1
    if has_uppercase(password):
        score += 1
    if has_digit(password):
        score += 1
    if has_symbol(password):
        score += 1

    if score >= 5:
        return {"score": score, "label": "strong"}
    if score >= 3:
        return {"score": score, "label": "medium"}
    return {"score": score, "label": "weak"}
