// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function rangeSums(values: number[], queries: [number, number][]): number[] {
  // prefix[k] is the sum of the first k values.
  const prefix = new Array<number>(values.length + 1);
  prefix[0] = 0;
  for (let k = 0; k < values.length; k++) prefix[k + 1] = prefix[k] + values[k];
  return queries.map(([i, j]) => prefix[j + 1] - prefix[i]);
}
