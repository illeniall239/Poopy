def center(rows: list[list[float]]) -> list[list[float]]:
    """New rows with each column's mean subtracted; ValueError on empty or ragged input."""
    raise NotImplementedError


def covariance_matrix(rows: list[list[float]], ddof: int = 1) -> list[list[float]]:
    """d×d covariance of the columns, normalized by n - ddof; ValueError on bad input or n - ddof <= 0."""
    raise NotImplementedError
