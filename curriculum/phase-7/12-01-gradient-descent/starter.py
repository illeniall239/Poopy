from collections.abc import Callable


def gradient_descent(
    grad_f: Callable[[list[float]], list[float]], x0: list[float], lr: float, steps: int
) -> list[list[float]]:
    """Trajectory [x0, x1, ..., x_steps] of x -= lr * grad_f(x); ValueError if lr <= 0 or steps < 0."""
    raise NotImplementedError
