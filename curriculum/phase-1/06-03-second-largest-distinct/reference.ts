// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function secondLargest(nums: number[]): number | undefined {
  let largest = -Infinity;
  let second = -Infinity;
  for (const n of nums) {
    if (n > largest) {
      second = largest;
      largest = n;
    } else if (n < largest && n > second) {
      second = n;
    }
  }
  return second === -Infinity ? undefined : second;
}
