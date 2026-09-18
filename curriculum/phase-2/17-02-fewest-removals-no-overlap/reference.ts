// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function fewestRemovals(intervals: [number, number][]): number {
  const byEnd = [...intervals].sort((a, b) => a[1] - b[1]);
  let removed = 0;
  let lastEnd = -Infinity;
  for (const [start, end] of byEnd) {
    if (start < lastEnd) removed++;
    else lastEnd = end;
  }
  return removed;
}
