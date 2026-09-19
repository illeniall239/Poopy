def build_tree(X: list[list[float]], y: list, max_depth: int | None = None, min_samples: int = 2) -> dict:
    """Grow a Gini classification tree as nested dicts: {"value": label} leaves, {"feature", "threshold", "left", "right"} nodes."""
    raise NotImplementedError


def predict_tree(tree: dict, x: list[float]):
    """Follow x down the tree (<= threshold goes left) and return the leaf's label."""
    raise NotImplementedError
