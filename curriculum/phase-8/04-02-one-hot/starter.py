def one_hot(values: list[str], vocabulary: list[str]) -> list[list[int]]:
    """0/1 rows in vocabulary order plus a final unknown-bucket column; ValueError on duplicate vocabulary."""
    raise NotImplementedError


def bucketize(x: float, boundaries: list[float]) -> int:
    """Index of x's bucket for strictly increasing boundaries; a value on a boundary goes above it."""
    raise NotImplementedError
