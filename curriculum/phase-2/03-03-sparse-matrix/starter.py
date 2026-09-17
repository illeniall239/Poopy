class SparseMatrix:
    """A rows x cols matrix that stores only its non-zero cells."""

    def __init__(self, rows: int, cols: int) -> None:
        """Create a rows x cols matrix of zeros."""
        raise NotImplementedError

    def set(self, row: int, col: int, value: int) -> None:
        """Set a cell; setting 0 removes it from storage."""
        raise NotImplementedError

    def get(self, row: int, col: int) -> int:
        """Return the cell's value, 0 if not stored."""
        raise NotImplementedError

    def non_zero_count(self) -> int:
        """Return how many cells are stored."""
        raise NotImplementedError

    def multiply_vector(self, vector: list[int]) -> list[int]:
        """Return the matrix times vector, in O(rows + non-zero cells)."""
        raise NotImplementedError
