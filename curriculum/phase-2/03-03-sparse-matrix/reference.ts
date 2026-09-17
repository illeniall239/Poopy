// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export class SparseMatrix {
  private readonly cells: Map<number, number>[];
  private count = 0;

  constructor(rows: number, cols: number) {
    this.cells = Array.from({ length: rows }, () => new Map<number, number>());
  }

  set(row: number, col: number, value: number): void {
    const cells = this.cells[row];
    const had = cells.has(col);
    if (value === 0) {
      if (had) {
        cells.delete(col);
        this.count--;
      }
      return;
    }
    if (!had) this.count++;
    cells.set(col, value);
  }

  get(row: number, col: number): number {
    return this.cells[row].get(col) ?? 0;
  }

  nonZeroCount(): number {
    return this.count;
  }

  multiplyVector(vector: number[]): number[] {
    return this.cells.map((cells) => {
      let sum = 0;
      for (const [col, value] of cells) sum += value * vector[col];
      return sum;
    });
  }
}
