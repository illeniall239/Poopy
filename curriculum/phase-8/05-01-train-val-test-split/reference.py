# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import random


def train_val_test_split(n: int, fracs: tuple[float, float, float], seed: int) -> tuple[list[int], list[int], list[int]]:
    if n < 0:
        raise ValueError("n must be >= 0")
    if len(fracs) != 3 or any(f < 0 for f in fracs) or abs(sum(fracs) - 1.0) > 1e-9:
        raise ValueError("fracs must be three non-negative numbers summing to 1")
    order = list(range(n))
    random.Random(seed).shuffle(order)
    train_frac, val_frac, _ = fracs
    c1 = round(n * train_frac)
    c2 = round(n * (train_frac + val_frac))
    return order[:c1], order[c1:c2], order[c2:]
