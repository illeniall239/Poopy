// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function longestConsecutiveRun(values: number[]): number {
  const present = new Set(values);
  let best = 0;
  for (const start of present) {
    if (present.has(start - 1)) continue;
    let length = 1;
    while (present.has(start + length)) length++;
    if (length > best) best = length;
  }
  return best;
}
