# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
DIGITS = "0123456789abcdef"


def to_base(n: int, base: int) -> str:
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        n, remainder = divmod(n, base)
        digits.append(DIGITS[remainder])
    return "".join(reversed(digits))


def from_base(text: str, base: int) -> int:
    value = 0
    for ch in text:
        value = value * base + DIGITS.index(ch)
    return value
