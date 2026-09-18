// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function compressRuns(text: string): string {
  let result = "";
  let i = 0;
  while (i < text.length) {
    const ch = text[i];
    let count = 0;
    while (i < text.length && text[i] === ch) {
      count++;
      i++;
    }
    result += count > 1 ? `${ch}${count}` : ch;
  }
  return result;
}
