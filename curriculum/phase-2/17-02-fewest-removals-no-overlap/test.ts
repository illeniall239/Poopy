import { test } from "node:test";
import assert from "node:assert/strict";
import { fewestRemovals } from "./solution.ts";

test("one interval overlaps two others", () => {
  assert.equal(fewestRemovals([[1, 2], [2, 3], [3, 4], [1, 3]]), 1);
});

test("identical intervals overlap each other", () => {
  assert.equal(fewestRemovals([[1, 2], [1, 2], [1, 2]]), 2);
});

test("touching intervals do not overlap", () => {
  assert.equal(fewestRemovals([[1, 2], [2, 3]]), 0);
});

test("one long interval covering several short ones", () => {
  assert.equal(fewestRemovals([[1, 10], [2, 3], [4, 5], [6, 7]]), 1);
});

test("empty array and single interval", () => {
  assert.equal(fewestRemovals([]), 0);
  assert.equal(fewestRemovals([[5, 9]]), 0);
});

test("negative coordinates", () => {
  assert.equal(fewestRemovals([[-5, -1], [-3, 2], [0, 4], [3, 6]]), 2);
});

test("nested intervals", () => {
  assert.equal(fewestRemovals([[1, 100], [2, 50], [3, 25], [4, 10]]), 3);
});

test("unsorted input is not changed", () => {
  const intervals: [number, number][] = [[3, 4], [1, 2], [2, 3]];
  assert.equal(fewestRemovals(intervals), 0);
  assert.deepEqual(intervals, [[3, 4], [1, 2], [2, 3]]);
});

test("200000 intervals in O(n log n)", () => {
  const K = 100000;
  const intervals: [number, number][] = [];
  for (let i = 0; i < 2 * K; i++) {
    const idx = (i * 7919) % (2 * K);
    const k = idx >> 1;
    intervals.push(idx % 2 === 0 ? [2 * k, 2 * k + 2] : [2 * k + 1, 2 * k + 3]);
  }
  assert.equal(fewestRemovals(intervals), K);
});
