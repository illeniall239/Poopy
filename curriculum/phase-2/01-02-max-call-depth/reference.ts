// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function maxCallDepth(calls: Record<string, string[]>, entry: string): number {
  const finished = new Map<string, number>();
  const onStack = new Set<string>();

  function depthFrom(fn: string): number {
    const known = finished.get(fn);
    if (known !== undefined) return known;
    if (onStack.has(fn)) return -1;
    onStack.add(fn);
    let deepest = 0;
    for (const callee of Object.hasOwn(calls, fn) ? calls[fn] : []) {
      const depth = depthFrom(callee);
      if (depth === -1) return -1;
      deepest = Math.max(deepest, depth);
    }
    onStack.delete(fn);
    finished.set(fn, deepest + 1);
    return deepest + 1;
  }

  return depthFrom(entry);
}
