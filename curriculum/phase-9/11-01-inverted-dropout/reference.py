# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import random


def dropout(x: list[float], p: float, rng: random.Random, training: bool) -> list[float]:
    if not 0 <= p < 1:
        raise ValueError("p must be in [0, 1)")
    if not training:
        return [float(v) for v in x]
    scale = 1.0 / (1.0 - p)
    return [0.0 if rng.random() < p else v * scale for v in x]
