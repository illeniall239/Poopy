def mse(y_true: list[float], y_pred: list[float]) -> float:
    """Mean squared error; ValueError on empty or mismatched lists."""
    raise NotImplementedError


def mae(y_true: list[float], y_pred: list[float]) -> float:
    """Mean absolute error; ValueError on empty or mismatched lists."""
    raise NotImplementedError


def rmse(y_true: list[float], y_pred: list[float]) -> float:
    """Root mean squared error; ValueError on empty or mismatched lists."""
    raise NotImplementedError


def r2(y_true: list[float], y_pred: list[float]) -> float:
    """1 - SS_res / SS_tot; ValueError on empty or mismatched lists or constant y_true."""
    raise NotImplementedError
