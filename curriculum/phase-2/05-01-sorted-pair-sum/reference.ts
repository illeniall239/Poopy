// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function sortedPairSum(values: number[], target: number): [number, number] | null {
  let lo = 0;
  let hi = values.length - 1;
  while (lo < hi) {
    const sum = values[lo] + values[hi];
    if (sum === target) return [values[lo], values[hi]];
    if (sum < target) lo++;
    else hi--;
  }
  return null;
}
