// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function isPalindrome(text: string): boolean {
  let letters = "";
  for (const ch of text.toLowerCase()) {
    if (ch >= "a" && ch <= "z") letters += ch;
  }
  for (let i = 0, j = letters.length - 1; i < j; i++, j--) {
    if (letters[i] !== letters[j]) return false;
  }
  return true;
}
