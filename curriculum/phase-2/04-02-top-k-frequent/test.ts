import { test } from "node:test";
import assert from "node:assert/strict";
import { topKFrequent } from "./solution.ts";

test("most frequent first", () => {
  assert.deepEqual(topKFrequent([1, 1, 1, 2, 2, 3], 2), [1, 2]);
});

test("k = 1 gives the single most frequent value", () => {
  assert.deepEqual(topKFrequent([4, 5, 5, 6], 1), [5]);
});

test("ties go to the value that appears first", () => {
  assert.deepEqual(topKFrequent([9, 4, 4, 9, 1], 2), [9, 4]);
  assert.deepEqual(topKFrequent([4, 9, 9, 4, 1], 2), [4, 9]);
});

test("frequency beats first appearance", () => {
  assert.deepEqual(topKFrequent([3, 1, 1, 3, 2, 2, 2], 3), [2, 3, 1]);
});

test("all distinct values keep their order", () => {
  assert.deepEqual(topKFrequent([5, 3, 8, 1], 3), [5, 3, 8]);
});

test("negative values and zero", () => {
  assert.deepEqual(topKFrequent([-1, -1, 0, 0, 0, 2], 2), [0, -1]);
});

test("k equal to the number of distinct values", () => {
  assert.deepEqual(topKFrequent([7, 8, 8, 9, 9, 9], 3), [9, 8, 7]);
});

test("does not change the input", () => {
  const values = [2, 1, 2];
  topKFrequent(values, 1);
  assert.deepEqual(values, [2, 1, 2]);
});

test("200000 values with 50000 distinct in O(n)", () => {
  const values = Array.from({ length: 200000 }, (_, i) => i % 50000);
  values.push(12345, 777, 12345, 777, 12345);
  assert.deepEqual(topKFrequent(values, 3), [12345, 777, 0]);
});
