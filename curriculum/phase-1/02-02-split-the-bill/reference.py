# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def split_bill(total_dollars: float, people: int) -> dict[str, int]:
    total_cents = round(total_dollars * 100)
    return {"shareCents": total_cents // people, "peopleWithExtraCent": total_cents % people}
