import { test } from "node:test";
import assert from "node:assert/strict";
import { maxSumFixedWindow } from "./solution.ts";

test("best window in the middle", () => {
  assert.equal(maxSumFixedWindow([2, 1, 5, 1, 3, 2], 3), 9);
});

test("best window at the end", () => {
  assert.equal(maxSumFixedWindow([2, 3, 4, 1, 5], 2), 7);
  assert.equal(maxSumFixedWindow([4, -1, 2, -7, 5, 6], 1), 6);
});

test("all negative values give a negative sum", () => {
  assert.equal(maxSumFixedWindow([-1, -2, -3, -4], 2), -3);
});

test("window covers the whole array", () => {
  assert.equal(maxSumFixedWindow([1, 2, 3], 3), 6);
  assert.equal(maxSumFixedWindow([5], 1), 5);
});

test("k larger than the array gives 0", () => {
  assert.equal(maxSumFixedWindow([1, 2], 3), 0);
  assert.equal(maxSumFixedWindow([], 1), 0);
});

test("all windows equal", () => {
  assert.equal(maxSumFixedWindow([3, 3, 3, 3], 2), 6);
});

test("does not change the input", () => {
  const values = [1, 2, 3];
  maxSumFixedWindow(values, 2);
  assert.deepEqual(values, [1, 2, 3]);
});

test("200000 values with a window of 100500 in O(n)", () => {
  const n = 200000;
  const values = Array.from({ length: n }, (_, i) => i % 1000);
  assert.equal(maxSumFixedWindow(values, 100500), 100 * 499500 + 374750);
});
