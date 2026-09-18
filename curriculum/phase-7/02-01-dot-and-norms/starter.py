def dot(a: list[float], b: list[float]) -> float:
    """Sum of elementwise products; ValueError on length mismatch."""
    raise NotImplementedError


def norm(v: list[float], p: int = 2) -> float:
    """L1 norm for p=1, L2 norm for p=2; ValueError for any other p."""
    raise NotImplementedError


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """dot(a, b) / (|a| |b|); ValueError on length mismatch or a zero-norm vector."""
    raise NotImplementedError
