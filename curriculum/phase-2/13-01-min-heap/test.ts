import { test } from "node:test";
import assert from "node:assert/strict";
import { MinHeap } from "./solution.ts";

function drain(heap: MinHeap): number[] {
  const out: number[] = [];
  while (heap.size() > 0) out.push(heap.pop()!);
  return out;
}

test("empty heap has size 0 and returns undefined", () => {
  const heap = new MinHeap();
  assert.equal(heap.size(), 0);
  assert.equal(heap.peek(), undefined);
  assert.equal(heap.pop(), undefined);
});

test("peek returns the smallest without removing it", () => {
  const heap = new MinHeap();
  heap.push(5);
  heap.push(3);
  heap.push(8);
  assert.equal(heap.peek(), 3);
  assert.equal(heap.size(), 3);
});

test("pops come out smallest first, duplicates included", () => {
  const heap = new MinHeap();
  for (const v of [5, 3, 8, 3, 1, 9, 2]) heap.push(v);
  assert.deepEqual(drain(heap), [1, 2, 3, 3, 5, 8, 9]);
  assert.equal(heap.pop(), undefined);
});

test("negative numbers", () => {
  const heap = new MinHeap();
  for (const v of [0, -4, 7, -10, 2]) heap.push(v);
  assert.deepEqual(drain(heap), [-10, -4, 0, 2, 7]);
});

test("interleaved push and pop", () => {
  const heap = new MinHeap();
  heap.push(4);
  heap.push(7);
  assert.equal(heap.pop(), 4);
  heap.push(1);
  heap.push(6);
  assert.equal(heap.pop(), 1);
  assert.equal(heap.peek(), 6);
  assert.equal(heap.size(), 2);
});

test("builds from a starting array without changing it", () => {
  const values = [9, 4, 7, 1, 8, 2];
  const heap = new MinHeap(values);
  assert.equal(heap.size(), 6);
  assert.deepEqual(drain(heap), [1, 2, 4, 7, 8, 9]);
  assert.deepEqual(values, [9, 4, 7, 1, 8, 2]);
});

test("200 000 pushes then pops, O(log n) each", () => {
  const n = 200000;
  const heap = new MinHeap();
  const values: number[] = [];
  for (let i = 0; i < n; i++) {
    const v = (i * 7919) % 200003;
    values.push(v);
    heap.push(v);
  }
  values.sort((a, b) => a - b);
  assert.deepEqual(drain(heap), values);
});
