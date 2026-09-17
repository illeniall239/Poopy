import { test } from "node:test";
import assert from "node:assert/strict";
import { zeroSumTriplets } from "./solution.ts";

test("two triplets in lexicographic order", () => {
  assert.deepEqual(zeroSumTriplets([-1, 0, 1, 2, -1, -4]), [[-1, -1, 2], [-1, 0, 1]]);
});

test("all zeros give one triplet", () => {
  assert.deepEqual(zeroSumTriplets([0, 0, 0]), [[0, 0, 0]]);
  assert.deepEqual(zeroSumTriplets([0, 0, 0, 0]), [[0, 0, 0]]);
});

test("a repeated value may be used twice in one triplet", () => {
  assert.deepEqual(zeroSumTriplets([-2, 0, 1, 1, 2]), [[-2, 0, 2], [-2, 1, 1]]);
});

test("duplicates of the first value don't repeat a triplet", () => {
  assert.deepEqual(zeroSumTriplets([3, -1, -2, -2, 4, -1, 0]), [[-2, -2, 4], [-2, -1, 3]]);
});

test("no triplet gives an empty array", () => {
  assert.deepEqual(zeroSumTriplets([1, 2, -2, -1]), []);
  assert.deepEqual(zeroSumTriplets([1, 2, 3]), []);
});

test("fewer than three values give an empty array", () => {
  assert.deepEqual(zeroSumTriplets([]), []);
  assert.deepEqual(zeroSumTriplets([0]), []);
  assert.deepEqual(zeroSumTriplets([1, -1]), []);
});

test("does not change the input", () => {
  const values = [2, -1, -1, 0];
  zeroSumTriplets(values);
  assert.deepEqual(values, [2, -1, -1, 0]);
});

test("3000 values with two triplets in O(n^2)", () => {
  const n = 3000;
  const values = Array.from({ length: n - 2 }, (_, i) => i + 1);
  values.push(-3, -2);
  assert.deepEqual(zeroSumTriplets(values), [[-3, -2, 5], [-3, 1, 2]]);
});
