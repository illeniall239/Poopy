export function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  throw new Error("Not implemented");
}

export function applyPatch<T>(original: T, patch: Partial<T>): T {
  throw new Error("Not implemented");
}
