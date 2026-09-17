# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def to_clock(total_seconds: int) -> str:
    hours = total_seconds // 3600
    minutes = total_seconds // 60 % 60
    seconds = total_seconds % 60
    return f"{two_digits(hours)}:{two_digits(minutes)}:{two_digits(seconds)}"


def two_digits(n: int) -> str:
    return f"{n // 10}{n % 10}"
