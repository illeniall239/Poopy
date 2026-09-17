import { test } from "node:test";
import assert from "node:assert/strict";
import { mergeSort } from "./solution.ts";

test("sorts a small array with a duplicate", () => {
  assert.deepEqual(mergeSort([5, 2, 9, 1, 5, 6]), [1, 2, 5, 5, 6, 9]);
});

test("compares as numbers, not as strings", () => {
  assert.deepEqual(mergeSort([10, 9, 100, 1]), [1, 9, 10, 100]);
});

test("negative numbers and zero", () => {
  assert.deepEqual(mergeSort([-3, 0, -7, 4, -1000000000, 1000000000]), [-1000000000, -7, -3, 0, 4, 1000000000]);
});

test("empty and single-element arrays", () => {
  assert.deepEqual(mergeSort([]), []);
  assert.deepEqual(mergeSort([42]), [42]);
});

test("already sorted, reversed and all equal", () => {
  assert.deepEqual(mergeSort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5]);
  assert.deepEqual(mergeSort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5]);
  assert.deepEqual(mergeSort([7, 7, 7, 7]), [7, 7, 7, 7]);
});

test("odd length where one half has leftovers", () => {
  assert.deepEqual(mergeSort([8, 1, 9, 2, 10, 3, 11]), [1, 2, 3, 8, 9, 10, 11]);
});

test("returns a new array and leaves the input unchanged", () => {
  const nums = [3, 1, 2];
  const result = mergeSort(nums);
  assert.deepEqual(result, [1, 2, 3]);
  assert.deepEqual(nums, [3, 1, 2]);
  assert.notEqual(result, nums);
});

test("300000 shuffled numbers in O(n log n)", () => {
  const n = 300000;
  const nums = Array.from({ length: n }, (_, i) => ((i * 7919 + 13) % 1000003) - 500000);
  const expected = nums.slice().sort((a, b) => a - b);
  const result = mergeSort(nums);
  assert.equal(result.length, n);
  assert.ok(result.every((v, i) => v === expected[i]), "result is not sorted correctly");
});
