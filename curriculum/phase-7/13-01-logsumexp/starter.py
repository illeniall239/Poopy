def logsumexp(xs: list[float]) -> float:
    """log(sum(exp(x))) computed stably by shifting by the maximum; ValueError on an empty list."""
    raise NotImplementedError


def log_softmax(xs: list[float]) -> list[float]:
    """x_i - logsumexp(xs) for every entry."""
    raise NotImplementedError


def softmax(xs: list[float]) -> list[float]:
    """exp of log_softmax; stable for very large or very small logits."""
    raise NotImplementedError
