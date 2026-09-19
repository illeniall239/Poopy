Net = tuple[list[list[float]], list[float], list[list[float]], list[float]]


def xor_net() -> Net:
    """Return hand-set (W1, b1, W2, b2) for a 2-2-1 ReLU network that computes XOR."""
    raise NotImplementedError


def predict(x: list[float], net: Net) -> int:
    """Forward pass with ReLU hidden units and a raw output; return 1 if output > 0.5 else 0."""
    raise NotImplementedError
