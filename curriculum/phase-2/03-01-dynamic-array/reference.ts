// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export class DynamicArray<T> {
  private storage: (T | undefined)[] = new Array(1);
  private count = 0;

  size(): number {
    return this.count;
  }

  capacity(): number {
    return this.storage.length;
  }

  push(value: T): void {
    if (this.count === this.storage.length) {
      const bigger: (T | undefined)[] = new Array(this.storage.length * 2);
      for (let i = 0; i < this.count; i++) bigger[i] = this.storage[i];
      this.storage = bigger;
    }
    this.storage[this.count++] = value;
  }

  get(index: number): T {
    this.checkIndex(index);
    return this.storage[index] as T;
  }

  set(index: number, value: T): void {
    this.checkIndex(index);
    this.storage[index] = value;
  }

  pop(): T {
    if (this.count === 0) throw new RangeError("pop from empty DynamicArray");
    const value = this.storage[--this.count] as T;
    this.storage[this.count] = undefined;
    return value;
  }

  toArray(): T[] {
    const result: T[] = [];
    for (let i = 0; i < this.count; i++) result.push(this.storage[i] as T);
    return result;
  }

  private checkIndex(index: number): void {
    if (index < 0 || index >= this.count) throw new RangeError(`index ${index} out of range`);
  }
}
