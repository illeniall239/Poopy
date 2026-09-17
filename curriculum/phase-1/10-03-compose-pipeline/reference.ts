// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export type Step = (n: number) => number;

export function pipeline(steps: Step[]): Step {
  const fixedSteps = [...steps];
  return (n) => fixedSteps.reduce((value, step) => step(value), n);
}

export function when(predicate: (n: number) => boolean, step: Step): Step {
  return (n) => (predicate(n) ? step(n) : n);
}
