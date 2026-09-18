// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function zeroSumTriplets(values: number[]): number[][] {
  const sorted = [...values].sort((a, b) => a - b);
  const result: number[][] = [];
  for (let i = 0; i + 2 < sorted.length; i++) {
    if (i > 0 && sorted[i] === sorted[i - 1]) continue;
    let lo = i + 1;
    let hi = sorted.length - 1;
    while (lo < hi) {
      const sum = sorted[i] + sorted[lo] + sorted[hi];
      if (sum < 0) lo++;
      else if (sum > 0) hi--;
      else {
        result.push([sorted[i], sorted[lo], sorted[hi]]);
        lo++;
        while (lo < hi && sorted[lo] === sorted[lo - 1]) lo++;
        hi--;
      }
    }
  }
  return result;
}
