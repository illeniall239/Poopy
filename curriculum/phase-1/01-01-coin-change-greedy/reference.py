# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def make_change(cents: int) -> dict[str, int]:
    quarters, cents = divmod(cents, 25)
    dimes, cents = divmod(cents, 10)
    nickels, pennies = divmod(cents, 5)
    return {"quarters": quarters, "dimes": dimes, "nickels": nickels, "pennies": pennies}
