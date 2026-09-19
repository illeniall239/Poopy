def label_smoothed_targets(k: int, target: int, eps: float) -> list[float]:
    """Return a length-k target: eps / k everywhere, plus 1 - eps on the target class."""
    raise NotImplementedError
