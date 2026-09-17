import { test } from "node:test";
import assert from "node:assert/strict";
import { sortedPairSum } from "./solution.ts";

test("finds a pair in the middle", () => {
  assert.deepEqual(sortedPairSum([1, 2, 3, 4, 6], 6), [2, 4]);
});

test("smallest first value wins", () => {
  assert.deepEqual(sortedPairSum([1, 2, 3, 4], 5), [1, 4]);
  assert.deepEqual(sortedPairSum([0, 1, 2, 3, 4, 5], 5), [0, 5]);
});

test("a position can't be used twice", () => {
  assert.deepEqual(sortedPairSum([2, 3, 4], 6), [2, 4]);
  assert.equal(sortedPairSum([1, 3, 7], 6), null);
});

test("equal values at two positions form a pair", () => {
  assert.deepEqual(sortedPairSum([3, 3], 6), [3, 3]);
  assert.deepEqual(sortedPairSum([1, 4, 4, 9], 8), [4, 4]);
});

test("negative values and zero", () => {
  assert.deepEqual(sortedPairSum([-5, -2, 0, 4, 9], 2), [-2, 4]);
  assert.deepEqual(sortedPairSum([-3, 0, 0, 3], 0), [-3, 3]);
});

test("no pair gives null", () => {
  assert.equal(sortedPairSum([1, 2, 3], 100), null);
  assert.equal(sortedPairSum([], 0), null);
  assert.equal(sortedPairSum([7], 14), null);
});

test("does not change the input", () => {
  const values = [1, 2, 3];
  sortedPairSum(values, 4);
  assert.deepEqual(values, [1, 2, 3]);
});

test("extreme values", () => {
  assert.deepEqual(sortedPairSum([-1000000000, 0, 1000000000], 0), [-1000000000, 1000000000]);
});

test("200000 even values with an odd target in O(n)", () => {
  const n = 200000;
  const values = Array.from({ length: n }, (_, i) => 2 * i);
  assert.equal(sortedPairSum(values, 2 * n - 3), null);
});
