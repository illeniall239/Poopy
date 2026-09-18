// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export class KthLargest {
  private k: number;
  private heap: number[] = [];

  constructor(k: number) {
    this.k = k;
  }

  add(value: number): number | undefined {
    const h = this.heap;
    if (h.length < this.k) {
      h.push(value);
      let i = h.length - 1;
      while (i > 0) {
        const parent = Math.floor((i - 1) / 2);
        if (h[parent] <= h[i]) break;
        [h[parent], h[i]] = [h[i], h[parent]];
        i = parent;
      }
    } else if (value > h[0]) {
      h[0] = value;
      let i = 0;
      while (true) {
        const l = 2 * i + 1;
        const r = l + 1;
        let smallest = i;
        if (l < h.length && h[l] < h[smallest]) smallest = l;
        if (r < h.length && h[r] < h[smallest]) smallest = r;
        if (smallest === i) break;
        [h[smallest], h[i]] = [h[i], h[smallest]];
        i = smallest;
      }
    }
    return h.length === this.k ? h[0] : undefined;
  }
}
