export type Result = { ok: true; value: number } | { ok: false; error: string };

export type Pair = { a: number; b: number };

export function safeDivide(a: number, b: number): Result {
  throw new Error("Not implemented");
}

export function sumOfQuotients(pairs: Pair[]): Result {
  throw new Error("Not implemented");
}
