# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import random
from collections import Counter


def bootstrap_sample(n: int, rng: random.Random) -> tuple[list[int], list[int]]:
    if n < 1:
        raise ValueError("n must be at least 1")
    in_bag = [rng.randrange(n) for _ in range(n)]
    drawn = set(in_bag)
    out_of_bag = [i for i in range(n) if i not in drawn]
    return in_bag, out_of_bag


def bagged_predict(models: list, x, mode: str = "vote"):
    if not models:
        raise ValueError("need at least one model")
    predictions = [model(x) for model in models]
    if mode == "mean":
        return sum(predictions) / len(predictions)
    if mode == "vote":
        counts = Counter(predictions)
        top = max(counts.values())
        return min(p for p, c in counts.items() if c == top)
    raise ValueError(f"unknown mode {mode!r}")
