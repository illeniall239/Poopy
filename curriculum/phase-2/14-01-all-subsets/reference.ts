// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function subsets(nums: number[]): number[][] {
  const result: number[][] = [];
  const path: number[] = [];

  function explore(i: number): void {
    if (i === nums.length) {
      result.push(path.slice());
      return;
    }
    path.push(nums[i]);
    explore(i + 1);
    path.pop();
    explore(i + 1);
  }

  explore(0);
  return result;
}
