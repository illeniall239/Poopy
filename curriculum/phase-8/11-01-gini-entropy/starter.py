def gini(labels: list) -> float:
    """Return the Gini impurity 1 - sum(p_k^2) of the labels; ValueError if empty."""
    raise NotImplementedError


def entropy(labels: list) -> float:
    """Return the entropy in bits -sum(p_k log2 p_k) of the labels; ValueError if empty."""
    raise NotImplementedError
