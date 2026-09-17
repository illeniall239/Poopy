// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function smallestCoveringWindow(s: string, t: string): string {
  if (t.length === 0 || s.length < t.length) return "";
  const need = new Map<string, number>();
  for (const ch of t) need.set(ch, (need.get(ch) ?? 0) + 1);
  let missing = need.size;
  const have = new Map<string, number>();
  let bestStart = 0;
  let bestLength = Infinity;
  let left = 0;
  for (let right = 0; right < s.length; right++) {
    const ch = s[right];
    if (!need.has(ch)) continue;
    const count = (have.get(ch) ?? 0) + 1;
    have.set(ch, count);
    if (count === need.get(ch)) missing--;
    while (missing === 0) {
      if (right - left + 1 < bestLength) {
        bestStart = left;
        bestLength = right - left + 1;
      }
      const out = s[left++];
      if (need.has(out)) {
        const remaining = have.get(out)! - 1;
        have.set(out, remaining);
        if (remaining < need.get(out)!) missing++;
      }
    }
  }
  return bestLength === Infinity ? "" : s.slice(bestStart, bestStart + bestLength);
}
