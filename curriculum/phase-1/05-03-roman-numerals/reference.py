# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def repeat(symbol: str, times: int) -> str:
    result = ""
    for _ in range(times):
        result += symbol
    return result


def digit_to_roman(digit: int, one: str, five: str, ten: str) -> str:
    if digit == 9:
        return one + ten
    if digit >= 5:
        return five + repeat(one, digit - 5)
    if digit == 4:
        return one + five
    return repeat(one, digit)


def to_roman(n: float) -> str:
    if n != int(n) or n < 1 or n > 3999:
        return ""
    n = int(n)
    return (
        repeat("M", n // 1000)
        + digit_to_roman(n // 100 % 10, "C", "D", "M")
        + digit_to_roman(n // 10 % 10, "X", "L", "C")
        + digit_to_roman(n % 10, "I", "V", "X")
    )
