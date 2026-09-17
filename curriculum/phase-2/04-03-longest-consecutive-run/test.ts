import { test } from "node:test";
import assert from "node:assert/strict";
import { longestConsecutiveRun } from "./solution.ts";

test("finds a run among unrelated values", () => {
  assert.equal(longestConsecutiveRun([100, 4, 200, 1, 3, 2]), 4);
});

test("run spread over the whole array", () => {
  assert.equal(longestConsecutiveRun([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]), 9);
});

test("no two values are consecutive", () => {
  assert.equal(longestConsecutiveRun([10, 30, 20]), 1);
  assert.equal(longestConsecutiveRun([5]), 1);
});

test("negative values", () => {
  assert.equal(longestConsecutiveRun([-1, 0, 1, -3, -2]), 5);
});

test("duplicates count once", () => {
  assert.equal(longestConsecutiveRun([1, 2, 2, 3]), 3);
  assert.equal(longestConsecutiveRun([7, 7, 7]), 1);
});

test("empty array gives 0", () => {
  assert.equal(longestConsecutiveRun([]), 0);
});

test("picks the longest of several runs", () => {
  assert.equal(longestConsecutiveRun([9, 1, 4, 2, 10, 11, 12, 3, 20]), 4);
});

test("does not change the input", () => {
  const values = [3, 1, 2];
  longestConsecutiveRun(values);
  assert.deepEqual(values, [3, 1, 2]);
});

test("200000 shuffled consecutive values in O(n)", () => {
  const n = 200000;
  const values = Array.from({ length: n }, (_, i) => ((i * 7919) % n) - 1000);
  assert.equal(longestConsecutiveRun(values), n);
});
