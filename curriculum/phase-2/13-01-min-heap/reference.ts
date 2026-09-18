// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export class MinHeap {
  private items: number[];

  constructor(values: number[] = []) {
    this.items = values.slice();
    for (let i = Math.floor(this.items.length / 2) - 1; i >= 0; i--) this.siftDown(i);
  }

  push(value: number): void {
    const a = this.items;
    a.push(value);
    let i = a.length - 1;
    while (i > 0) {
      const parent = Math.floor((i - 1) / 2);
      if (a[parent] <= a[i]) break;
      [a[parent], a[i]] = [a[i], a[parent]];
      i = parent;
    }
  }

  pop(): number | undefined {
    const a = this.items;
    if (a.length === 0) return undefined;
    const top = a[0];
    const last = a.pop()!;
    if (a.length > 0) {
      a[0] = last;
      this.siftDown(0);
    }
    return top;
  }

  peek(): number | undefined {
    return this.items[0];
  }

  size(): number {
    return this.items.length;
  }

  private siftDown(i: number): void {
    const a = this.items;
    while (true) {
      const l = 2 * i + 1;
      const r = 2 * i + 2;
      let smallest = i;
      if (l < a.length && a[l] < a[smallest]) smallest = l;
      if (r < a.length && a[r] < a[smallest]) smallest = r;
      if (smallest === i) return;
      [a[smallest], a[i]] = [a[i], a[smallest]];
      i = smallest;
    }
  }
}
