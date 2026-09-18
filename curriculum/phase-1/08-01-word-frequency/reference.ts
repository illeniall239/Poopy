// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function wordFrequency(text: string): Map<string, number> {
  const counts = new Map<string, number>();
  let word = "";
  for (const ch of text.toLowerCase() + " ") {
    if (ch >= "a" && ch <= "z") {
      word += ch;
    } else if (word !== "") {
      const current = counts.get(word);
      counts.set(word, current === undefined ? 1 : current + 1);
      word = "";
    }
  }
  return counts;
}
