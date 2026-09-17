// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
type Entry<V> = [string, V];

export class StringHashMap<V> {
  private buckets: Entry<V>[][] = StringHashMap.emptyBuckets<V>(8);
  private count = 0;

  private static emptyBuckets<V>(n: number): Entry<V>[][] {
    return Array.from({ length: n }, () => []);
  }

  private bucketFor(key: string, buckets: Entry<V>[][]): Entry<V>[] {
    let hash = 0;
    for (let i = 0; i < key.length; i++) hash = (hash * 31 + key.charCodeAt(i)) >>> 0;
    return buckets[hash % buckets.length];
  }

  set(key: string, value: V): void {
    const bucket = this.bucketFor(key, this.buckets);
    for (const entry of bucket) {
      if (entry[0] === key) {
        entry[1] = value;
        return;
      }
    }
    bucket.push([key, value]);
    this.count++;
    if (this.count / this.buckets.length > 0.75) this.resize();
  }

  get(key: string): V | undefined {
    for (const [k, v] of this.bucketFor(key, this.buckets)) if (k === key) return v;
    return undefined;
  }

  has(key: string): boolean {
    return this.bucketFor(key, this.buckets).some(([k]) => k === key);
  }

  delete(key: string): boolean {
    const bucket = this.bucketFor(key, this.buckets);
    const index = bucket.findIndex(([k]) => k === key);
    if (index === -1) return false;
    bucket[index] = bucket[bucket.length - 1];
    bucket.pop();
    this.count--;
    return true;
  }

  size(): number {
    return this.count;
  }

  bucketCount(): number {
    return this.buckets.length;
  }

  private resize(): void {
    const bigger = StringHashMap.emptyBuckets<V>(this.buckets.length * 2);
    for (const bucket of this.buckets) {
      for (const entry of bucket) this.bucketFor(entry[0], bigger).push(entry);
    }
    this.buckets = bigger;
  }
}
