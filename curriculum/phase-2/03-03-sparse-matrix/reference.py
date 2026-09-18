# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
class SparseMatrix:
    def __init__(self, rows: int, cols: int) -> None:
        self._cells: list[dict[int, int]] = [{} for _ in range(rows)]
        self._count = 0

    def set(self, row: int, col: int, value: int) -> None:
        cells = self._cells[row]
        had = col in cells
        if value == 0:
            if had:
                del cells[col]
                self._count -= 1
            return
        if not had:
            self._count += 1
        cells[col] = value

    def get(self, row: int, col: int) -> int:
        return self._cells[row].get(col, 0)

    def non_zero_count(self) -> int:
        return self._count

    def multiply_vector(self, vector: list[int]) -> list[int]:
        return [sum(value * vector[col] for col, value in cells.items()) for cells in self._cells]
