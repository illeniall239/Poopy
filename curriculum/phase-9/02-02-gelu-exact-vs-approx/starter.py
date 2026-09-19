def gelu_exact(x: float) -> float:
    """Return 0.5 * x * (1 + erf(x / sqrt(2)))."""
    raise NotImplementedError


def gelu_tanh(x: float) -> float:
    """Return the tanh approximation 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x**3)))."""
    raise NotImplementedError
