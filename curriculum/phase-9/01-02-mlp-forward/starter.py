from typing import Callable

Layer = tuple[list[list[float]], list[float], Callable[[float], float]]


def mlp_forward(x: list[float], layers: list[Layer]) -> list[float]:
    """Apply each (W, b, act) layer in turn to x and return the final output list."""
    raise NotImplementedError
