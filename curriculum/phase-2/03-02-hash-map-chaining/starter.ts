export class StringHashMap<V> {
  set(key: string, value: V): void {
    throw new Error("Not implemented");
  }

  get(key: string): V | undefined {
    throw new Error("Not implemented");
  }

  has(key: string): boolean {
    throw new Error("Not implemented");
  }

  delete(key: string): boolean {
    throw new Error("Not implemented");
  }

  size(): number {
    throw new Error("Not implemented");
  }

  bucketCount(): number {
    throw new Error("Not implemented");
  }
}
