# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def fraction_dead(pre_acts: list[list[float]]) -> float:
    rows = [list(r) for r in pre_acts]
    if not rows or not rows[0]:
        raise ValueError("need at least one row and one column")
    if any(len(r) != len(rows[0]) for r in rows):
        raise ValueError("rows must all have the same length")
    columns = list(zip(*rows))  # one tuple per unit
    dead = sum(1 for unit in columns if all(z <= 0 for z in unit))
    return dead / len(columns)
