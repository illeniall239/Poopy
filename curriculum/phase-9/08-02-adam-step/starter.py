def adam_step(params: list[float], grads: list[float], state: dict[str, list[float]],
              lr: float, b1: float, b2: float, eps: float, t: int) -> list[float]:
    """One bias-corrected Adam step at 1-based step t; update params and state in place, return params."""
    raise NotImplementedError
