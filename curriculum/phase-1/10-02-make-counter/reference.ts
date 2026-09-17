// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export type Counter = {
  increment: () => number;
  decrement: () => number;
  reset: () => number;
  value: () => number;
};

export function makeCounter(start: number = 0, step: number = 1): Counter {
  let count = start;
  return {
    increment: () => (count += step),
    decrement: () => (count -= step),
    reset: () => (count = start),
    value: () => count,
  };
}
