def matrix_rank(a: list[list[float]], tol: float = 1e-9) -> int:
    """Number of pivots in the row echelon form of a, treating |pivot| <= tol as zero."""
    raise NotImplementedError


def is_singular(a: list[list[float]], tol: float = 1e-9) -> bool:
    """True when the square matrix a has rank below its size; ValueError if not square."""
    raise NotImplementedError
