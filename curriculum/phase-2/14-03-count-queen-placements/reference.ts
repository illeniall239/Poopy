// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function countQueens(n: number): number {
  const cols = new Set<number>();
  const downDiagonals = new Set<number>();
  const upDiagonals = new Set<number>();

  function place(row: number): number {
    if (row === n) return 1;
    let count = 0;
    for (let col = 0; col < n; col++) {
      if (cols.has(col) || downDiagonals.has(row - col) || upDiagonals.has(row + col)) continue;
      cols.add(col);
      downDiagonals.add(row - col);
      upDiagonals.add(row + col);
      count += place(row + 1);
      cols.delete(col);
      downDiagonals.delete(row - col);
      upDiagonals.delete(row + col);
    }
    return count;
  }

  return place(0);
}
