# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def count_queens(n: int) -> int:
    cols: set[int] = set()
    down_diagonals: set[int] = set()
    up_diagonals: set[int] = set()

    def place(row: int) -> int:
        if row == n:
            return 1
        count = 0
        for col in range(n):
            if col in cols or row - col in down_diagonals or row + col in up_diagonals:
                continue
            cols.add(col)
            down_diagonals.add(row - col)
            up_diagonals.add(row + col)
            count += place(row + 1)
            cols.remove(col)
            down_diagonals.remove(row - col)
            up_diagonals.remove(row + col)
        return count

    return place(0)
