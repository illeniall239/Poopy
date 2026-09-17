// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function pairWithTargetSum(values: number[], target: number): [number, number] {
  const firstIndexOf = new Map<number, number>();
  for (let j = 0; j < values.length; j++) {
    const i = firstIndexOf.get(target - values[j]);
    if (i !== undefined) return [i, j];
    if (!firstIndexOf.has(values[j])) firstIndexOf.set(values[j], j);
  }
  return [-1, -1];
}
