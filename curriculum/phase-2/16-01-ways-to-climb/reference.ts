// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function climbWays(n: number): number {
  let twoBelow = 1; // ways to reach step i - 2
  let oneBelow = 1; // ways to reach step i - 1
  for (let i = 2; i <= n; i++) {
    const current = oneBelow + twoBelow;
    twoBelow = oneBelow;
    oneBelow = current;
  }
  return oneBelow;
}
