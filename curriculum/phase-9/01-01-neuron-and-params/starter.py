from typing import Callable


def neuron(x: list[float], w: list[float], b: float, act: Callable[[float], float]) -> float:
    """Return act(sum(x_i * w_i) + b); raise ValueError if x and w differ in length."""
    raise NotImplementedError


def count_params(layer_sizes: list[int]) -> int:
    """Return the number of weights plus biases of a fully connected MLP with these layer widths."""
    raise NotImplementedError
