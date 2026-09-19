def gradient_boost_stumps(xs: list[float], ys: list[float], n_rounds: int, lr: float) -> dict:
    """Boost depth-1 stumps on the residuals; return {"base", "lr", "stumps", "losses"}."""
    raise NotImplementedError


def predict_boosted(model: dict, x: float) -> float:
    """base + lr * sum of every stump's value at x."""
    raise NotImplementedError
