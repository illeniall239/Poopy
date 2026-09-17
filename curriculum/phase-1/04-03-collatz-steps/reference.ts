// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export type CollatzResult = { steps: number; peak: number };

export function collatzSteps(n: number): CollatzResult {
  let steps = 0;
  let peak = n;
  while (n !== 1) {
    n = n % 2 === 0 ? n / 2 : 3 * n + 1;
    steps++;
    if (n > peak) peak = n;
  }
  return { steps, peak };
}
