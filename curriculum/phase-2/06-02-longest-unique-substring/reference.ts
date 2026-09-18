// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function longestUniqueSubstring(s: string): number {
  const lastSeen = new Map<string, number>();
  let best = 0;
  let left = 0;
  for (let right = 0; right < s.length; right++) {
    const ch = s[right];
    const previous = lastSeen.get(ch);
    if (previous !== undefined && previous >= left) left = previous + 1;
    lastSeen.set(ch, right);
    if (right - left + 1 > best) best = right - left + 1;
  }
  return best;
}
