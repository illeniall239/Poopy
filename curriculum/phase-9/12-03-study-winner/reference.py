# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math
from typing import Any, Hashable


def study_winner(runs: list[dict[str, Any]], scientific_param: str, metric: str) -> tuple[Hashable, dict[Hashable, float]]:
    # For each scientific value keep the sort key of its best run: lowest metric, fewest steps, earliest run.
    best: dict[Hashable, tuple[float, int, int]] = {}
    for i, run in enumerate(runs):
        value = run["metrics"].get(metric)
        if value is None or math.isnan(value):
            continue
        key = (value, run["steps"], i)
        sci = run["config"][scientific_param]
        if sci not in best or key < best[sci]:
            best[sci] = key
    if not best:
        raise ValueError("no usable runs")
    winner = min(best, key=best.__getitem__)
    return winner, {sci: key[0] for sci, key in best.items()}
