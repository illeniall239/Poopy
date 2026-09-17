export function dedupe(items: number[]): number[] {
  const seen = new Set<number>();
  for (let i = 0; i < items.length; i++) {
    if (seen.has(items[i])) {
      items.splice(i, 1);
    } else {
      seen.add(items[i]);
    }
  }
  return items;
}
