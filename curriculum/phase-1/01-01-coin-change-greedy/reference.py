# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def make_change(cents: int) -> dict[str, int]:
    quarters, cents = divmod(cents, 25)
    dimes, cents = divmod(cents, 10)
    nickels, pennies = divmod(cents, 5)
    return {"quarters": quarters, "dimes": dimes, "nickels": nickels, "pennies": pennies}
