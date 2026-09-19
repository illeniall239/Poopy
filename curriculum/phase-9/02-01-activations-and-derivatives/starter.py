def sigmoid(x: float) -> float:
    """Return 1 / (1 + e^-x) without overflowing for large |x|."""
    raise NotImplementedError


def d_sigmoid(x: float) -> float:
    """Return the derivative of sigmoid at x."""
    raise NotImplementedError


def tanh(x: float) -> float:
    """Return tanh(x)."""
    raise NotImplementedError


def d_tanh(x: float) -> float:
    """Return the derivative of tanh at x."""
    raise NotImplementedError


def relu(x: float) -> float:
    """Return max(0, x)."""
    raise NotImplementedError


def d_relu(x: float) -> float:
    """Return 1 for x > 0, else 0 (including at x = 0)."""
    raise NotImplementedError


def leaky_relu(x: float, alpha: float = 0.01) -> float:
    """Return x if x > 0 else alpha * x."""
    raise NotImplementedError


def d_leaky_relu(x: float, alpha: float = 0.01) -> float:
    """Return 1 for x > 0, else alpha (including at x = 0)."""
    raise NotImplementedError


def gelu(x: float) -> float:
    """Return the exact GELU x * Phi(x), with Phi the standard normal CDF."""
    raise NotImplementedError


def d_gelu(x: float) -> float:
    """Return the derivative of the exact GELU at x."""
    raise NotImplementedError
