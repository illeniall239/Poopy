import random


def stratified_split(labels: list, val_frac: float, seed: int) -> tuple[list[int], list[int]]:
    """Sorted (train, val) indices with each class's val share within ±1 row of count * val_frac."""
    raise NotImplementedError


def time_series_splits(n: int, n_splits: int) -> list[tuple[list[int], list[int]]]:
    """Expanding-window (train, val) splits where each val block follows its train block."""
    raise NotImplementedError
