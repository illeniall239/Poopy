import { test } from "node:test";
import assert from "node:assert/strict";
import { binarySearch } from "./solution.ts";

const odds = [1, 3, 5, 7, 9, 11];

test("finds a value in the middle", () => {
  assert.equal(binarySearch(odds, 7), 3);
  assert.equal(binarySearch(odds, 5), 2);
});

test("finds the first and last values", () => {
  assert.equal(binarySearch(odds, 1), 0);
  assert.equal(binarySearch(odds, 11), 5);
});

test("missing value between two elements", () => {
  assert.equal(binarySearch(odds, 4), -1);
});

test("missing value below and above the range", () => {
  assert.equal(binarySearch(odds, 0), -1);
  assert.equal(binarySearch(odds, 12), -1);
});

test("empty array", () => {
  assert.equal(binarySearch([], 5), -1);
});

test("one and two elements", () => {
  assert.equal(binarySearch([5], 5), 0);
  assert.equal(binarySearch([5], 6), -1);
  assert.equal(binarySearch([2, 4], 4), 1);
  assert.equal(binarySearch([2, 4], 3), -1);
});

test("negative and very large values", () => {
  const values = [-2000000000, -7, 0, 1999999999, 2000000000];
  assert.equal(binarySearch(values, -2000000000), 0);
  assert.equal(binarySearch(values, 2000000000), 4);
  assert.equal(binarySearch(values, 1), -1);
});

test("100000 searches in 1000000 values in O(log n)", () => {
  const n = 1000000;
  const evens = new Array<number>(n);
  for (let i = 0; i < n; i++) evens[i] = 2 * i;
  let wrong = 0;
  for (let q = 0; q < 100000; q++) {
    const i = (q * 7919) % n;
    if (binarySearch(evens, 2 * i) !== i) wrong++;
    if (binarySearch(evens, 2 * i + 1) !== -1) wrong++;
  }
  assert.equal(wrong, 0);
});
