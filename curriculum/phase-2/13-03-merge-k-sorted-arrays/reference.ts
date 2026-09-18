// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
type Entry = { value: number; array: number; index: number };

export function mergeKSorted(arrays: number[][]): number[] {
  const heap: Entry[] = [];

  const push = (e: Entry) => {
    heap.push(e);
    let i = heap.length - 1;
    while (i > 0) {
      const parent = Math.floor((i - 1) / 2);
      if (heap[parent].value <= heap[i].value) break;
      [heap[parent], heap[i]] = [heap[i], heap[parent]];
      i = parent;
    }
  };

  const pop = (): Entry => {
    const top = heap[0];
    const last = heap.pop()!;
    if (heap.length > 0) {
      heap[0] = last;
      let i = 0;
      while (true) {
        const l = 2 * i + 1;
        const r = l + 1;
        let smallest = i;
        if (l < heap.length && heap[l].value < heap[smallest].value) smallest = l;
        if (r < heap.length && heap[r].value < heap[smallest].value) smallest = r;
        if (smallest === i) break;
        [heap[smallest], heap[i]] = [heap[i], heap[smallest]];
        i = smallest;
      }
    }
    return top;
  };

  arrays.forEach((arr, a) => {
    if (arr.length > 0) push({ value: arr[0], array: a, index: 0 });
  });
  const out: number[] = [];
  while (heap.length > 0) {
    const { value, array, index } = pop();
    out.push(value);
    if (index + 1 < arrays[array].length) push({ value: arrays[array][index + 1], array, index: index + 1 });
  }
  return out;
}
