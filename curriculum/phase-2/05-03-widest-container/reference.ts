// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function widestContainer(heights: number[]): number {
  let lo = 0;
  let hi = heights.length - 1;
  let best = 0;
  while (lo < hi) {
    const area = (hi - lo) * Math.min(heights[lo], heights[hi]);
    if (area > best) best = area;
    if (heights[lo] < heights[hi]) lo++;
    else hi--;
  }
  return best;
}
