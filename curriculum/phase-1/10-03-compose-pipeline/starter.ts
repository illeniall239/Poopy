export type Step = (n: number) => number;

export function pipeline(steps: Step[]): Step {
  throw new Error("Not implemented");
}

export function when(predicate: (n: number) => boolean, step: Step): Step {
  throw new Error("Not implemented");
}
