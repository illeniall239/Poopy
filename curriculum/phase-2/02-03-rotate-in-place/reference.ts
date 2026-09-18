// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
function reverse(values: number[], from: number, to: number): void {
  while (from < to) {
    const temp = values[from];
    values[from] = values[to];
    values[to] = temp;
    from++;
    to--;
  }
}

export function rotateRight(values: number[], k: number): void {
  const n = values.length;
  if (n === 0) return;
  const steps = k % n;
  reverse(values, 0, n - 1);
  reverse(values, 0, steps - 1);
  reverse(values, steps, n - 1);
}
