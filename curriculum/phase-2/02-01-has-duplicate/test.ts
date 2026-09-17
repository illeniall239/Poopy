import { test } from "node:test";
import assert from "node:assert/strict";
import { hasDuplicate } from "./solution.ts";

test("finds a repeated value", () => {
  assert.equal(hasDuplicate([1, 2, 3, 1]), true);
});

test("all distinct values", () => {
  assert.equal(hasDuplicate([1, 2, 3]), false);
});

test("empty array has no duplicates", () => {
  assert.equal(hasDuplicate([]), false);
});

test("a single value is not a duplicate of itself", () => {
  assert.equal(hasDuplicate([7]), false);
});

test("negative values and their opposites are different", () => {
  assert.equal(hasDuplicate([-1, 1, -2, 2, 0]), false);
  assert.equal(hasDuplicate([-5, 3, -5]), true);
});

test("duplicates as the last two values", () => {
  assert.equal(hasDuplicate([4, 8, 15, 16, 23, 42, 42]), true);
});

test("does not change the input", () => {
  const values = [3, 1, 2, 3];
  hasDuplicate(values);
  assert.deepEqual(values, [3, 1, 2, 3]);
});

test("200000 distinct values in O(n)", () => {
  const n = 200000;
  const values = Array.from({ length: n }, (_, i) => (i * 7919) % n);
  assert.equal(hasDuplicate(values), false);
});
