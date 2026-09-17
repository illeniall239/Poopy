// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function power(base: number, exp: number): number {
  if (exp === 0) return 1;
  const half = power(base, Math.floor(exp / 2));
  return exp % 2 === 0 ? half * half : half * half * base;
}
