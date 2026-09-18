// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function canReachLastIndex(jumps: number[]): boolean {
  let farthest = 0;
  for (let i = 0; i <= farthest && i < jumps.length; i++) {
    farthest = Math.max(farthest, i + jumps[i]);
  }
  return farthest >= jumps.length - 1;
}
