// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>; // the one allowed `as`: {} starts out missing the keys the loop fills in
  for (const key of keys) {
    result[key] = obj[key];
  }
  return result;
}

export function applyPatch<T>(original: T, patch: Partial<T>): T {
  const result = { ...original };
  for (const key in patch) {
    const value = patch[key];
    if (value !== undefined) result[key] = value;
  }
  return result;
}
