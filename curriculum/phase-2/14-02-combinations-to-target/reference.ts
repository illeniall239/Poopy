// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function combinationsToTarget(candidates: number[], target: number): number[][] {
  const sorted = [...candidates].sort((a, b) => a - b);
  const result: number[][] = [];
  const path: number[] = [];

  function explore(start: number, remaining: number): void {
    if (remaining === 0) {
      result.push(path.slice());
      return;
    }
    for (let i = start; i < sorted.length && sorted[i] <= remaining; i++) {
      path.push(sorted[i]);
      explore(i, remaining - sorted[i]);
      path.pop();
    }
  }

  explore(0, target);
  return result;
}
