# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import random
from collections import defaultdict


def stratified_split(labels: list, val_frac: float, seed: int) -> tuple[list[int], list[int]]:
    if not labels:
        raise ValueError("no labels")
    if not 0 < val_frac < 1:
        raise ValueError("val_frac must be strictly between 0 and 1")
    by_class = defaultdict(list)
    for i, label in enumerate(labels):
        by_class[label].append(i)
    rng = random.Random(seed)
    train, val = [], []
    for indices in by_class.values():  # first-seen class order, so the split is reproducible
        rng.shuffle(indices)
        cut = round(len(indices) * val_frac)
        val.extend(indices[:cut])
        train.extend(indices[cut:])
    return sorted(train), sorted(val)


def time_series_splits(n: int, n_splits: int) -> list[tuple[list[int], list[int]]]:
    if n_splits < 1 or n < n_splits + 1:
        raise ValueError("need n_splits >= 1 and n >= n_splits + 1")
    test_size = n // (n_splits + 1)
    splits = []
    for i in range(n_splits):
        start = n - (n_splits - i) * test_size
        splits.append((list(range(start)), list(range(start, start + test_size))))
    return splits
