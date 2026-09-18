def mse(w: float, b: float, xs: list[float], ys: list[float]) -> float:
    """Mean squared error of the line w*x + b on (xs, ys); ValueError on mismatch or empty data."""
    raise NotImplementedError


def mse_gradient(w: float, b: float, xs: list[float], ys: list[float]) -> tuple[float, float]:
    """(dL/dw, dL/db) of the MSE for the line w*x + b."""
    raise NotImplementedError
