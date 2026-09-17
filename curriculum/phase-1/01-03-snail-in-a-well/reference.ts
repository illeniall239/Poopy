// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function daysToEscape(depth: number, climb: number, slide: number): number {
  if (climb >= depth) return 1;
  if (climb <= slide) return -1;
  // Before the last day the snail must reach depth - climb; each full day gains climb - slide.
  return Math.ceil((depth - climb) / (climb - slide)) + 1;
}
