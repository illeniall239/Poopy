// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
const ALPHABET = "abcdefghijklmnopqrstuvwxyz";

export function caesarShift(text: string, shift: number): string {
  let result = "";
  for (const ch of text) {
    const lower = ch.toLowerCase();
    const index = ALPHABET.indexOf(lower);
    if (index === -1) {
      result += ch;
      continue;
    }
    const shifted = ALPHABET[(((index + shift) % 26) + 26) % 26];
    result += ch === lower ? shifted : shifted.toUpperCase();
  }
  return result;
}
