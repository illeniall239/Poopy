# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
class RangeError(ValueError):
    """Raised when the age is a whole number but outside 0 to 150."""


def parse_age(input: str) -> int:
    text = input.strip()
    if text == "":
        raise ValueError("Age is empty")
    for ch in text:
        if ch < "0" or ch > "9":
            raise ValueError(f'Age must be a whole number, got "{input}"')
    age = int(text)
    if age > 150:
        raise RangeError(f"Age must be between 0 and 150, got {age}")
    return age
