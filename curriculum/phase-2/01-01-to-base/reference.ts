// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
const DIGITS = "0123456789abcdef";

export function toBase(n: number, base: number): string {
  if (n === 0) return "0";
  const digits: string[] = [];
  while (n > 0) {
    digits.push(DIGITS[n % base]);
    n = Math.floor(n / base);
  }
  return digits.reverse().join("");
}

export function fromBase(text: string, base: number): number {
  let value = 0;
  for (const ch of text) value = value * base + DIGITS.indexOf(ch);
  return value;
}
