export class DynamicArray<T> {
  size(): number {
    throw new Error("Not implemented");
  }

  capacity(): number {
    throw new Error("Not implemented");
  }

  push(value: T): void {
    throw new Error("Not implemented");
  }

  get(index: number): T {
    throw new Error("Not implemented");
  }

  set(index: number, value: T): void {
    throw new Error("Not implemented");
  }

  pop(): T {
    throw new Error("Not implemented");
  }

  toArray(): T[] {
    throw new Error("Not implemented");
  }
}
