// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export class TwoStackQueue<T> {
  private incoming: T[] = [];
  private outgoing: T[] = [];

  enqueue(value: T): void {
    this.incoming.push(value);
  }

  dequeue(): T | undefined {
    this.refill();
    return this.outgoing.pop();
  }

  peek(): T | undefined {
    this.refill();
    return this.outgoing[this.outgoing.length - 1];
  }

  size(): number {
    return this.incoming.length + this.outgoing.length;
  }

  private refill(): void {
    if (this.outgoing.length > 0) return;
    while (this.incoming.length > 0) this.outgoing.push(this.incoming.pop() as T);
  }
}
