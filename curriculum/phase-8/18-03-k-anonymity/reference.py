# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from collections import Counter

MASK = "*"


def k_anonymity(records: list[dict], quasi_ids: list[str]) -> int:
    if not records:
        raise ValueError("no records")
    classes = Counter(tuple(r[q] for q in quasi_ids) for r in records)
    return min(classes.values())


def _apply(records: list[dict], quasi_ids: list[str], rules: dict, levels: dict[str, int]) -> list[dict]:
    out = []
    for record in records:
        new = dict(record)
        for q in quasi_ids:
            funcs = rules.get(q, [])
            level = levels[q]
            if level == len(funcs) + 1:
                new[q] = MASK
            elif level > 0:
                new[q] = funcs[level - 1](record[q])  # always from the original value
        out.append(new)
    return out


def generalize(records: list[dict], quasi_ids: list[str], rules: dict, k: int) -> list[dict]:
    if not records:
        raise ValueError("no records")
    if k < 1:
        raise ValueError("k must be at least 1")
    levels = {q: 0 for q in quasi_ids}
    max_level = {q: len(rules.get(q, [])) + 1 for q in quasi_ids}
    while True:
        current = _apply(records, quasi_ids, rules, levels)
        if k_anonymity(current, quasi_ids) >= k:
            return current
        open_columns = [q for q in quasi_ids if levels[q] < max_level[q]]
        if not open_columns:
            raise ValueError(f"cannot reach {k}-anonymity with {len(records)} records")
        next_q = min(open_columns, key=lambda q: levels[q])  # min keeps the earliest on ties
        levels[next_q] += 1
