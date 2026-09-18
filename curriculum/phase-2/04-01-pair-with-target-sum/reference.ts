// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function pairWithTargetSum(values: number[], target: number): [number, number] {
  const firstIndexOf = new Map<number, number>();
  for (let j = 0; j < values.length; j++) {
    const i = firstIndexOf.get(target - values[j]);
    if (i !== undefined) return [i, j];
    if (!firstIndexOf.has(values[j])) firstIndexOf.set(values[j], j);
  }
  return [-1, -1];
}
