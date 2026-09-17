// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export type Nested = number | Nested[];

export function flatten(items: Nested[]): number[] {
  const result: number[] = [];
  for (const item of items) {
    if (Array.isArray(item)) result.push(...flatten(item));
    else result.push(item);
  }
  return result;
}

export function depth(items: Nested[]): number {
  let deepestInner = 0;
  for (const item of items) {
    if (Array.isArray(item)) deepestInner = Math.max(deepestInner, depth(item));
  }
  return 1 + deepestInner;
}
