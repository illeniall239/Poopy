// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function permutations(s: string): string[] {
  if (s.length === 0) return [""];
  const results = new Set<string>();
  for (let i = 0; i < s.length; i++) {
    const rest = s.slice(0, i) + s.slice(i + 1);
    for (const tail of permutations(rest)) results.add(s[i] + tail);
  }
  return [...results].sort();
}
