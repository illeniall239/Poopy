// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export type MaxMin = { max: number; min: number };

export function maxAndMin(nums: number[]): MaxMin | undefined {
  if (nums.length === 0) return undefined;
  let max = nums[0];
  let min = nums[0];
  for (const n of nums) {
    if (n > max) max = n;
    if (n < min) min = n;
  }
  return { max, min };
}
