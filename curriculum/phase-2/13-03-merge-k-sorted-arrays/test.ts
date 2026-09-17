import { test } from "node:test";
import assert from "node:assert/strict";
import { mergeKSorted } from "./solution.ts";

test("three interleaving arrays", () => {
  assert.deepEqual(mergeKSorted([[1, 4, 7], [2, 5, 8], [3, 6, 9]]), [1, 2, 3, 4, 5, 6, 7, 8, 9]);
});

test("empty inner arrays and duplicates", () => {
  assert.deepEqual(mergeKSorted([[], [1, 1, 3], [], [1, 2]]), [1, 1, 1, 2, 3]);
});

test("no arrays at all", () => {
  assert.deepEqual(mergeKSorted([]), []);
});

test("a single array", () => {
  assert.deepEqual(mergeKSorted([[-3, 0, 2]]), [-3, 0, 2]);
});

test("negatives and different lengths", () => {
  assert.deepEqual(mergeKSorted([[-10, -5, 0, 5], [-7], [1, 2, 3, 4, 100]]), [-10, -7, -5, 0, 1, 2, 3, 4, 5, 100]);
});

test("does not change the input arrays", () => {
  const input = [[1, 3], [2, 4]];
  mergeKSorted(input);
  assert.deepEqual(input, [[1, 3], [2, 4]]);
});

test("10 000 arrays of 20 values, O(N log k)", () => {
  const k = 10000;
  const m = 20;
  const arrays: number[][] = [];
  for (let j = 0; j < k; j++) {
    const arr: number[] = [];
    for (let i = 0; i < m; i++) arr.push(i * k + j);
    arrays.push(arr);
  }
  const result = mergeKSorted(arrays);
  assert.equal(result.length, k * m);
  assert.ok(result.every((v, i) => v === i), "values are not 0, 1, 2, ... in order");
});
