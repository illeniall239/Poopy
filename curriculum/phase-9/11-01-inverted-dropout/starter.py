import random


def dropout(x: list[float], p: float, rng: random.Random, training: bool) -> list[float]:
    """Inverted dropout: in training, zero each element with probability p and scale survivors by 1/(1-p); identity in eval."""
    raise NotImplementedError
