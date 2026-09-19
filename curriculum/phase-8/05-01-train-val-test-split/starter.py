import random


def train_val_test_split(n: int, fracs: tuple[float, float, float], seed: int) -> tuple[list[int], list[int], list[int]]:
    """Seeded shuffle of 0..n-1 cut at cumulative rounded fractions into disjoint (train, val, test)."""
    raise NotImplementedError
