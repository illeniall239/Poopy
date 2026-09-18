from collections.abc import Callable


def minimize_1d(
    f: Callable[[float], float],
    x0: float,
    lr: float,
    tol: float = 1e-8,
    max_steps: int = 10_000,
    h: float = 1e-5,
) -> tuple[float, int]:
    """Gradient descent with a central-difference gradient; stops when |grad| < tol or after max_steps."""
    raise NotImplementedError
