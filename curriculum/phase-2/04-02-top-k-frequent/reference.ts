// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export function topKFrequent(values: number[], k: number): number[] {
  const counts = new Map<number, number>();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);

  // byCount[c] holds the values seen exactly c times, in first-appearance order (Map keeps insertion order).
  const byCount: number[][] = Array.from({ length: values.length + 1 }, () => []);
  for (const [value, count] of counts) byCount[count].push(value);

  const result: number[] = [];
  for (let count = values.length; count >= 1 && result.length < k; count--) {
    for (const value of byCount[count]) {
      if (result.length === k) break;
      result.push(value);
    }
  }
  return result;
}
