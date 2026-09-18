// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function maxSumFixedWindow(values: number[], k: number): number {
  if (values.length < k) return 0;
  let sum = 0;
  for (let i = 0; i < k; i++) sum += values[i];
  let best = sum;
  for (let i = k; i < values.length; i++) {
    sum += values[i] - values[i - k];
    if (sum > best) best = sum;
  }
  return best;
}
