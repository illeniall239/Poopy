import random


def bootstrap_sample(n: int, rng: random.Random) -> tuple[list[int], list[int]]:
    """Return (n indices drawn with replacement via rng.randrange(n), sorted out-of-bag indices)."""
    raise NotImplementedError


def bagged_predict(models: list, x, mode: str = "vote"):
    """Combine model(x) over all models by majority vote (ties to the smallest) or by the mean."""
    raise NotImplementedError
