# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Callable


def neuron(x: list[float], w: list[float], b: float, act: Callable[[float], float]) -> float:
    if len(x) != len(w):
        raise ValueError("x and w must have the same length")
    return act(sum(xi * wi for xi, wi in zip(x, w)) + b)


def count_params(layer_sizes: list[int]) -> int:
    return sum(n_in * n_out + n_out for n_in, n_out in zip(layer_sizes, layer_sizes[1:]))
