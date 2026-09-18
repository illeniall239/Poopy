// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function dedupe(items: number[]): number[] {
  const seen = new Set<number>();
  const result: number[] = [];
  for (let i = 0; i < items.length; i++) {
    if (!seen.has(items[i])) {
      seen.add(items[i]);
      result.push(items[i]);
    }
  }
  return result;
}
