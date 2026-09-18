// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function quickSort(nums: number[]): void {
  sortRange(nums, 0, nums.length - 1);
}

function sortRange(nums: number[], lo: number, hi: number): void {
  while (lo < hi) {
    const pivot = nums[lo + Math.floor(Math.random() * (hi - lo + 1))];
    // Three regions: [lo, lt) < pivot, [lt, i) === pivot, (gt, hi] > pivot.
    let lt = lo;
    let gt = hi;
    let i = lo;
    while (i <= gt) {
      if (nums[i] < pivot) swap(nums, i++, lt++);
      else if (nums[i] > pivot) swap(nums, i, gt--);
      else i++;
    }
    // Recurse into the smaller side and loop on the larger one to keep the stack O(log n).
    if (lt - lo < hi - gt) {
      sortRange(nums, lo, lt - 1);
      lo = gt + 1;
    } else {
      sortRange(nums, gt + 1, hi);
      hi = lt - 1;
    }
  }
}

function swap(nums: number[], a: number, b: number): void {
  const t = nums[a];
  nums[a] = nums[b];
  nums[b] = t;
}
