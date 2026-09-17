// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export type Result = { ok: true; value: number } | { ok: false; error: string };

export type Pair = { a: number; b: number };

export function safeDivide(a: number, b: number): Result {
  if (!Number.isFinite(a) || !Number.isFinite(b)) return { ok: false, error: "Inputs must be finite numbers" };
  if (b === 0) return { ok: false, error: "Cannot divide by zero" };
  return { ok: true, value: a / b };
}

export function sumOfQuotients(pairs: Pair[]): Result {
  let sum = 0;
  for (let i = 0; i < pairs.length; i++) {
    const result = safeDivide(pairs[i].a, pairs[i].b);
    if (!result.ok) return { ok: false, error: `Pair ${i + 1}: ${result.error}` };
    sum += result.value;
  }
  return { ok: true, value: sum };
}
