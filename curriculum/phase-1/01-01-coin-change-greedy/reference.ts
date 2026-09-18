// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export type Change = { quarters: number; dimes: number; nickels: number; pennies: number };

export function makeChange(cents: number): Change {
  const quarters = Math.floor(cents / 25);
  cents %= 25;
  const dimes = Math.floor(cents / 10);
  cents %= 10;
  const nickels = Math.floor(cents / 5);
  return { quarters, dimes, nickels, pennies: cents % 5 };
}
