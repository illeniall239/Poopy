def sgd_momentum_step(params: list[float], grads: list[float], state: list[float], lr: float, beta: float) -> list[float]:
    """One SGD-with-momentum step: v = beta*v + g, p -= lr*v; update params and state in place, return state."""
    raise NotImplementedError
