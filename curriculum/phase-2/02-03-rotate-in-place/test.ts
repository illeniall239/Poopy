import { test } from "node:test";
import assert from "node:assert/strict";
import { rotateRight } from "./solution.ts";

function rotated(values: number[], k: number): number[] {
  const result = rotateRight(values, k);
  assert.equal(result, undefined);
  return values;
}

test("rotates the given array by 3", () => {
  assert.deepEqual(rotated([1, 2, 3, 4, 5, 6, 7], 3), [5, 6, 7, 1, 2, 3, 4]);
});

test("k = 0 leaves the array alone", () => {
  assert.deepEqual(rotated([1, 2, 3], 0), [1, 2, 3]);
});

test("k equal to the length is a full turn", () => {
  assert.deepEqual(rotated([1, 2, 3, 4], 4), [1, 2, 3, 4]);
});

test("k larger than the length wraps around", () => {
  assert.deepEqual(rotated([1, 2, 3], 10), [3, 1, 2]);
});

test("empty array stays empty", () => {
  assert.deepEqual(rotated([], 5), []);
});

test("single element", () => {
  assert.deepEqual(rotated([9], 4), [9]);
});

test("duplicates and negative values", () => {
  assert.deepEqual(rotated([-1, -1, 2, 0], 1), [0, -1, -1, 2]);
});

test("1000000 elements with a huge k in O(n)", () => {
  const n = 1000000;
  const values = Array.from({ length: n }, (_, i) => i);
  rotateRight(values, 1000000000 + 500000);
  let firstWrong = -1;
  for (let i = 0; i < n; i++) {
    if (values[i] !== (i + 500000) % n) {
      firstWrong = i;
      break;
    }
  }
  assert.equal(values.length, n);
  assert.equal(firstWrong, -1);
});
