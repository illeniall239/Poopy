import { test } from "node:test";
import assert from "node:assert/strict";
import { pairWithTargetSum } from "./solution.ts";

test("finds a simple pair", () => {
  assert.deepEqual(pairWithTargetSum([2, 7, 11, 15], 9), [0, 1]);
});

test("an element doesn't pair with itself", () => {
  assert.deepEqual(pairWithTargetSum([3, 2, 4], 6), [1, 2]);
});

test("equal values at two positions form a pair", () => {
  assert.deepEqual(pairWithTargetSum([3, 3], 6), [0, 1]);
});

test("smallest j wins, then smallest i", () => {
  assert.deepEqual(pairWithTargetSum([1, 3, 2, 4, 3], 6), [2, 3]);
  assert.deepEqual(pairWithTargetSum([2, 2, 4], 6), [0, 2]);
  assert.deepEqual(pairWithTargetSum([1, 5, 1, 5], 6), [0, 1]);
});

test("no pair gives [-1, -1]", () => {
  assert.deepEqual(pairWithTargetSum([5], 10), [-1, -1]);
  assert.deepEqual(pairWithTargetSum([], 0), [-1, -1]);
  assert.deepEqual(pairWithTargetSum([1, 2, 3], 100), [-1, -1]);
});

test("negative values and zero", () => {
  assert.deepEqual(pairWithTargetSum([-3, 4, 0, 3, 90], 0), [0, 3]);
  assert.deepEqual(pairWithTargetSum([0, 7, 0], 0), [0, 2]);
});

test("does not change the input", () => {
  const values = [4, 1, 3];
  pairWithTargetSum(values, 4);
  assert.deepEqual(values, [4, 1, 3]);
});

test("extreme values", () => {
  assert.deepEqual(pairWithTargetSum([-1000000000, 1000000000, -1000000000], -2000000000), [0, 2]);
});

test("200000 values with the only pair at the end in O(n)", () => {
  const n = 200000;
  const values = Array.from({ length: n }, (_, i) => i);
  assert.deepEqual(pairWithTargetSum(values, 2 * n - 3), [n - 2, n - 1]);
});
