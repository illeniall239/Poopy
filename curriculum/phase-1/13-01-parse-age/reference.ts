// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function parseAge(input: string): number {
  const text = input.trim();
  if (text === "") throw new Error("Age is empty");
  for (const ch of text) {
    if (ch < "0" || ch > "9") throw new Error(`Age must be a whole number, got "${input}"`);
  }
  const age = Number(text);
  if (age > 150) throw new RangeError(`Age must be between 0 and 150, got ${age}`);
  return age;
}
