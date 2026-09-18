def sigmoid(x: float) -> float:
    """1 / (1 + exp(-x)), safe for very large |x|."""
    raise NotImplementedError


def sigmoid_prime(x: float) -> float:
    """sigmoid(x) * (1 - sigmoid(x))."""
    raise NotImplementedError


def tanh(x: float) -> float:
    """Hyperbolic tangent."""
    raise NotImplementedError


def tanh_prime(x: float) -> float:
    """1 - tanh(x) ** 2."""
    raise NotImplementedError


def relu(x: float) -> float:
    """max(0, x)."""
    raise NotImplementedError


def relu_prime(x: float) -> float:
    """1.0 for x > 0, else 0.0."""
    raise NotImplementedError
