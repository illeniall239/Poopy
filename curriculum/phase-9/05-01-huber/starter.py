def huber(y: list[float], yhat: list[float], delta: float = 1.0) -> float:
    """Return the mean Huber loss of predictions yhat against targets y."""
    raise NotImplementedError


def huber_grad(y: list[float], yhat: list[float], delta: float = 1.0) -> list[float]:
    """Return the gradient of the mean Huber loss with respect to each yhat[i]."""
    raise NotImplementedError
