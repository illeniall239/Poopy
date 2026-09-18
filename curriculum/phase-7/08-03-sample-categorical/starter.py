import random


def sample_categorical(probs: list[float], n: int, rng: random.Random) -> list[int]:
    """n category indices drawn with the given probabilities, one rng.random() per draw; ValueError on bad input."""
    raise NotImplementedError


def empirical_frequencies(draws: list[int], k: int) -> list[float]:
    """Fraction of draws equal to each index 0..k-1."""
    raise NotImplementedError
