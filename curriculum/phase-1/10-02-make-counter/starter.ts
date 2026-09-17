export type Counter = {
  increment: () => number;
  decrement: () => number;
  reset: () => number;
  value: () => number;
};

export function makeCounter(start: number = 0, step: number = 1): Counter {
  throw new Error("Not implemented");
}
