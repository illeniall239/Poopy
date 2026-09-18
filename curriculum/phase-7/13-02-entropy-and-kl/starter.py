def entropy(p: list[float]) -> float:
    """-sum p_i log p_i in nats with 0 log 0 = 0; ValueError if p is not a distribution."""
    raise NotImplementedError


def cross_entropy(p: list[float], q: list[float]) -> float:
    """-sum p_i log q_i; inf if q is 0 where p is positive; ValueError on invalid input."""
    raise NotImplementedError


def kl(p: list[float], q: list[float]) -> float:
    """KL(p || q) = sum p_i log(p_i / q_i); inf if q is 0 where p is positive; ValueError on invalid input."""
    raise NotImplementedError
