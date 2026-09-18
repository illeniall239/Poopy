// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function countIslands(grid: string[]): number {
  const rows = grid.length;
  if (rows === 0) return 0;
  const cols = grid[0].length;
  const visited = new Uint8Array(rows * cols);
  let islands = 0;

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c] !== "1" || visited[r * cols + c]) continue;
      islands++;
      visited[r * cols + c] = 1;
      const stack = [r * cols + c];
      while (stack.length > 0) {
        const cell = stack.pop()!;
        const cr = Math.floor(cell / cols);
        const cc = cell % cols;
        for (const [nr, nc] of [[cr - 1, cc], [cr + 1, cc], [cr, cc - 1], [cr, cc + 1]]) {
          if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
          if (grid[nr][nc] !== "1" || visited[nr * cols + nc]) continue;
          visited[nr * cols + nc] = 1;
          stack.push(nr * cols + nc);
        }
      }
    }
  }
  return islands;
}
