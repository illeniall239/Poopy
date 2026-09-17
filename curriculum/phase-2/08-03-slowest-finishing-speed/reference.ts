// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function minShredSpeed(stacks: number[], h: number): number {
  let lo = 1;
  let hi = Math.max(...stacks);
  while (lo < hi) {
    const mid = lo + Math.floor((hi - lo) / 2);
    let hours = 0;
    for (const p of stacks) hours += Math.ceil(p / mid);
    if (hours <= h) hi = mid;
    else lo = mid + 1;
  }
  return lo;
}
