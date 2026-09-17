# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def shipping_cost(subtotal_cents: int, weight_kg: float, express: bool) -> int:
    if weight_kg > 30:
        return -1
    if subtotal_cents >= 5000 and not express and weight_kg <= 20:
        return 0

    if weight_kg <= 1:
        cost = 499
    elif weight_kg <= 5:
        cost = 899
    else:
        cost = 1499

    return cost + 1000 if express else cost
