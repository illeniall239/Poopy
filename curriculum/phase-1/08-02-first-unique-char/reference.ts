// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function firstUniqueIndex(text: string): number {
  const counts = new Map<string, number>();
  for (const ch of text) {
    const current = counts.get(ch);
    counts.set(ch, current === undefined ? 1 : current + 1);
  }
  for (let i = 0; i < text.length; i++) {
    if (counts.get(text[i]) === 1) return i;
  }
  return -1;
}
